# -*- coding: utf-8 -*-
# 导入必要的库
import os  # 操作系统接口
import jieba  # 中文分词工具
import dataclasses as dc  # 数据类
import functools  # 高阶函数工具
from collections.abc import Callable, Mapping, Sequence  # 抽象基类
from pathlib import Path  # 路径处理
from typing import Annotated, Any, Optional, Union  # 类型注解
import numpy as np  # 数值计算库
import ruamel.yaml as yaml  # YAML解析器
import torch  # PyTorch深度学习框架
import typer  # 命令行接口工具
from datasets import Dataset, DatasetDict, NamedSplit, Split, load_dataset  # 数据集处理
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu  # BLEU评分
from peft import (  # 参数高效微调工具
    PeftConfig,
    PeftModelForCausalLM,
    get_peft_config,
    get_peft_model
)
from rouge_chinese import Rouge  # 中文ROUGE评分
from torch import nn  # PyTorch神经网络模块
from transformers import (  # Hugging Face Transformers库
    AutoModelForCausalLM,
    AutoTokenizer,
    EvalPrediction,
    GenerationConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    Seq2SeqTrainingArguments, AutoConfig,
)
from transformers import DataCollatorForSeq2Seq as _DataCollatorForSeq2Seq  # 序列到序列数据整理器

from transformers import Seq2SeqTrainer as _Seq2SeqTrainer  # 序列到序列训练器

# 定义模型类型
ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
# 定义分词器类型
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]
# 创建Typer应用
app = typer.Typer(pretty_exceptions_show_locals=False)


# 自定义序列到序列数据整理器
class DataCollatorForSeq2Seq(_DataCollatorForSeq2Seq):
    def __call__(self, features, return_tensors=None):
        # 提取输出ID
        output_ids = (
            [feature['output_ids'] for feature in features]
            if 'output_ids' in features[0].keys()
            else None
        )
        if output_ids is not None:
            # 计算最大输出长度
            max_output_length = max(len(out) for out in output_ids)
            # 如果需要填充到特定倍数
            if self.pad_to_multiple_of is not None:
                max_output_length = (
                        (
                                max_output_length + self.pad_to_multiple_of - 1) //
                        self.pad_to_multiple_of * self.pad_to_multiple_of
                )
            # 对每个特征进行填充
            for feature in features:
                remainder = [self.tokenizer.pad_token_id] * (
                        max_output_length - len(feature['output_ids'])
                )
                if isinstance(feature['output_ids'], list):
                    feature['output_ids'] = feature['output_ids'] + remainder
                else:
                    feature['output_ids'] = np.concatenate(
                        [feature['output_ids'], remainder]
                    ).astype(np.int64)
        # 调用父类方法
        return super().__call__(features, return_tensors)


# 自定义序列到序列训练器
class Seq2SeqTrainer(_Seq2SeqTrainer):
    def prediction_step(
            self,
            model: nn.Module,
            inputs: dict[str, Any],
            prediction_loss_only: bool,
            ignore_keys=None,
            **gen_kwargs,
    ) -> tuple[Optional[float], Optional[torch.Tensor], Optional[torch.Tensor]]:
        # 如果使用生成进行预测，提取输出ID
        if self.args.predict_with_generate:
            output_ids = inputs.pop('output_ids')
        # 获取输入ID
        input_ids = inputs['input_ids']
        # 调用父类的预测步骤
        loss, generated_tokens, labels = super().prediction_step(
            model, inputs, prediction_loss_only, ignore_keys, **gen_kwargs
        )
        # 截取生成的tokens，只保留输入之后的部分
        generated_tokens = generated_tokens[:, input_ids.size()[1]:]
        # 如果使用生成进行预测，使用输出ID作为标签
        if self.args.predict_with_generate:
            labels = output_ids
        return loss, generated_tokens, labels
    # 对于P-Tuning，可以定义新的save_model函数来保存prefix_encoder模型
    # 但可能会导致加载整个模型时出现问题

    # def save_model(self, output_dir: Optional[str] = None, _internal_call: bool = False):
    #     if output_dir is None:
    #         output_dir = self.args.output_dir
    #     os.makedirs(output_dir, exist_ok=True)
    #     ptuning_params = {k: v for k, v in self.model.transformer.prefix_encoder.state_dict().items()}
    #
    #     torch.save(ptuning_params, os.path.join(output_dir, 'pytorch_model.bin'))
    #
    #     print(f"P-Tuning model weights saved in {output_dir}")
    #
    #     if self.tokenizer is not None:
    #         self.tokenizer.save_pretrained(output_dir)


# 解析路径，转换为绝对路径
def _resolve_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()


# 进行健全性检查，打印输入ID和输出ID的对应关系
def _sanity_check(
        input_ids: Sequence[int],
        output_ids: Sequence[int],
        tokenizer: PreTrainedTokenizer,
):
    print('--> Sanity check')
    for in_id, out_id in zip(input_ids, output_ids):
        if in_id == 0:
            continue
        if in_id in tokenizer.tokenizer.index_special_tokens:
            in_text = tokenizer.tokenizer.index_special_tokens[in_id]
        else:
            in_text = tokenizer.decode([in_id])
        print(f'{repr(in_text):>20}: {in_id} -> {out_id}')


# 获取YAML解析器，使用缓存避免重复创建
@functools.cache
def _get_yaml_parser() -> yaml.YAML:
    parser = yaml.YAML(typ='safe', pure=True)
    parser.indent(mapping=2, offset=2, sequence=4)
    parser.default_flow_style = False
    return parser


# 数据配置类
@dc.dataclass
class DataConfig(object):
    train_file: str  # 训练文件路径
    val_file: Optional[str] = None  # 验证文件路径
    test_file: Optional[str] = None  # 测试文件路径

    num_proc: Optional[int] = None  # 处理器数量

    @property
    def data_format(self) -> str:
        # 获取数据格式（文件后缀）
        return Path(self.train_file).suffix

    @property
    def data_files(self) -> dict[NamedSplit, str]:
        # 获取数据文件字典，键为分割名，值为文件路径
        return {
            split: data_file
            for split, data_file in zip(
                [Split.TRAIN, Split.VALIDATION, Split.TEST],
                [self.train_file, self.val_file, self.test_file],
            )
            if data_file is not None
        }


# 微调配置类
@dc.dataclass
class FinetuningConfig(object):
    data_config: DataConfig  # 数据配置

    max_input_length: int  # 最大输入长度
    max_output_length: int  # 最大输出长度

    training_args: Seq2SeqTrainingArguments = dc.field(  # 训练参数
        default_factory=lambda: Seq2SeqTrainingArguments(output_dir='./output')
    )
    peft_config: Optional[PeftConfig] = None  # PEFT配置

    def __post_init__(self):
        # 初始化后处理
        if not self.training_args.do_eval or self.data_config.val_file is None:
            # 如果不进行评估或没有验证文件，跳过评估阶段
            self.training_args.do_eval = False
            self.training_args.evaluation_strategy = 'no'
            self.data_config.val_file = None
        else:
            # 设置评估批次大小
            self.training_args.per_device_eval_batch_size = (
                    self.training_args.per_device_eval_batch_size
                    or self.training_args.per_device_train_batch_size
            )

    @classmethod
    def from_dict(cls, **kwargs) -> 'FinetuningConfig':
        # 从字典创建配置
        training_args = kwargs.get('training_args', None)
        if training_args is not None and not isinstance(
                training_args, Seq2SeqTrainingArguments
        ):
            gen_config = training_args.get('generation_config')
            # 处理生成配置
            if not isinstance(gen_config, GenerationConfig):
                training_args['generation_config'] = GenerationConfig(
                    **gen_config
                )
            kwargs['training_args'] = Seq2SeqTrainingArguments(**training_args)

        # 处理数据配置
        data_config = kwargs.get('data_config')
        if not isinstance(data_config, DataConfig):
            kwargs['data_config'] = DataConfig(**data_config)

        # 处理PEFT配置
        peft_config = kwargs.get('peft_config', None)
        if peft_config is not None and not isinstance(peft_config, PeftConfig):
            kwargs['peft_config'] = get_peft_config(peft_config)
        return cls(**kwargs)

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> 'FinetuningConfig':
        # 从文件加载配置
        path = _resolve_path(path) #变绝对路径
        kwargs = _get_yaml_parser().load(path)
        return cls.from_dict(**kwargs)


# 加载数据集
def _load_datasets(
        data_dir: Path,
        data_format: str,
        data_files: dict[NamedSplit, str],
        num_proc: Optional[int],
) -> DatasetDict:
    if data_format in ('.csv', '.json', '.jsonl'):
        # 加载CSV、JSON或JSONL格式的数据
        dataset_dct = load_dataset(
            data_format[1:],
            data_dir=data_dir,
            data_files=data_files,
            num_proc=num_proc,
        )
    else:
        # 不支持的格式抛出异常
        err_msg = f"Cannot load dataset in the '{data_format}' format."
        raise NotImplementedError(err_msg)

    return dataset_dct


# 数据管理器类
class DataManager(object):
    def __init__(self, data_dir: str, data_config: DataConfig):
        self._num_proc = data_config.num_proc

        # 加载数据集
        self._dataset_dct = _load_datasets(
            _resolve_path(data_dir),
            data_config.data_format,
            data_config.data_files,
            self._num_proc,
        )

    def _get_dataset(self, split: NamedSplit) -> Optional[Dataset]:
        # 获取指定分割的数据集
        return self._dataset_dct.get(split, None)

    def get_dataset(
            self,
            split: NamedSplit,
            process_fn: Callable[[dict[str, Any]], dict[str, Any]],
            batched: bool = True,
            remove_orig_columns: bool = True,
    ) -> Optional[Dataset]:
        # 获取并处理数据集
        orig_dataset = self._get_dataset(split)
        if orig_dataset is None:
            return

        # 决定是否移除原始列
        if remove_orig_columns:
            remove_columns = orig_dataset.column_names
        else:
            remove_columns = None
        # 应用处理函数
        return orig_dataset.map(
            process_fn,
            batched=batched,
            remove_columns=remove_columns,
            num_proc=self._num_proc,
        )


# 打印模型大小
def print_model_size(model: PreTrainedModel):
    print("--> Model")
    # 计算可训练参数数量
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n--> model has {total_params / 1e6}M params\n")


# 处理批次数据（用于训练）
def process_batch(
        batch: Mapping[str, Sequence],
        tokenizer: PreTrainedTokenizer,
        max_input_length: int,
        max_output_length: int,
) -> dict[str, list]:
    batched_tools = batch.get('tools', None)
    batched_conv = batch['conversations']
    batched_input_ids = []
    batched_labels = []

    # 如果没有工具，创建None列表
    if batched_tools is None:
        batched_tools = [None] * len(batched_conv)

    # 处理每个对话
    for tools, conv in zip(batched_tools, batched_conv):
        input_ids, loss_masks = [
            tokenizer.get_command('[gMASK]'),
            tokenizer.get_command('sop'),
        ], [False, False]

        # 如果有工具，抛出未实现异常
        if tools is not None:
            raise NotImplementedError()

        # 处理对话中的每条消息
        for message in conv:
            # 根据角色决定是否计算损失
            if message['role'] in ('system', 'user'):
                loss_mask_val = False
            else:
                loss_mask_val = True

            # 处理工具消息
            if message['role'] == 'tool':
                raise NotImplementedError()
            else:
                # 构建单条消息的输入ID
                new_input_ids = tokenizer.build_single_message(
                    message['role'], '', message['content']
                )
                new_loss_masks = [loss_mask_val] * len(new_input_ids)

            # 添加到输入ID和损失掩码
            input_ids += new_input_ids
            loss_masks += new_loss_masks

        # 添加结束标记
        input_ids.append(tokenizer.eos_token_id)
        # 调整损失掩码
        loss_masks = [False, *loss_masks]
        labels = []
        # 根据掩码创建标签
        for input_id, mask in zip(input_ids, loss_masks):
            if mask:
                labels.append(input_id)
            else:
                labels.append(-100)
        # 限制长度
        max_length = max_input_length + max_output_length + 1
        batched_input_ids.append(input_ids[:max_length])
        batched_labels.append(labels[:max_length])
    return {'input_ids': batched_input_ids, 'labels': batched_labels}


# 处理批次数据（用于评估）
def process_batch_eval(
        batch: Mapping[str, Sequence],
        tokenizer: PreTrainedTokenizer,
        max_input_length: int,
        max_output_length: int,
) -> dict[str, list]:
    batched_tools = batch.get('tools', None)
    batched_conv = batch['conversations']
    batched_input_ids = []
    # 不提供labels字段以避免计算损失
    batched_output_ids = []

    # 如果没有工具，创建None列表
    if batched_tools is None:
        batched_tools = [None] * len(batched_conv)

    # 处理每个对话
    for tools, conv in zip(batched_tools, batched_conv):
        input_ids = [
            tokenizer.get_command('[gMASK]'),
            tokenizer.get_command('sop'),
        ]

        # 如果有工具，抛出未实现异常
        if tools is not None:
            raise NotImplementedError()

        # 处理对话中的每条消息
        for message in conv:
            # 如果输入长度超过限制，跳出循环
            if len(input_ids) >= max_input_length:
                break
            # 处理工具消息
            if message['role'] == 'tool':
                raise NotImplementedError()
            else:
                # 构建单条消息的输入ID
                new_input_ids = tokenizer.build_single_message(
                    message['role'], '', message['content']
                )
                # 如果是助手消息，分离提示和输出
                if message['role'] == 'assistant':
                    output_prompt, output_ids = (
                        new_input_ids[:1],
                        new_input_ids[1:],
                    )
                    # 添加结束标记
                    output_ids.append(tokenizer.eos_token_id)
                    # 添加到批次
                    batched_input_ids.append(
                        input_ids[:max_input_length] + output_prompt[:1]
                    )
                    batched_output_ids.append(output_ids[:max_output_length])
                input_ids += new_input_ids
    return {'input_ids': batched_input_ids, 'output_ids': batched_output_ids}


# 准备模型进行训练
def _prepare_model_for_training(model: nn.Module, use_cpu: bool):
    # 将参数转换为fp32
    for param in model.parameters():
        if param.requires_grad or use_cpu:
            param.data = param.data.to(torch.float32)


# 加载分词器和模型
def load_tokenizer_and_model(
        model_dir: str,
        peft_config: Optional[PeftConfig] = None,
) -> tuple[PreTrainedTokenizer, nn.Module]:
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    if peft_config is not None:
        # 处理PREFIX_TUNING
        if peft_config.peft_type.name == "PREFIX_TUNING":
            config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)
            config.pre_seq_len = peft_config.num_virtual_tokens
            config.use_cache = False
            model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                trust_remote_code=True,
                config=config,
            )
        # 处理LORA
        if peft_config.peft_type.name == "LORA":
            model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                trust_remote_code=True,
                empty_init=False,
                use_cache=False
            )
            # 应用PEFT
            model = get_peft_model(model, peft_config)
            model.print_trainable_parameters()
    else:
        # 加载普通模型
        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            trust_remote_code=True,
            empty_init=False,
            use_cache=False
        )
    # 打印模型大小
    print_model_size(model)
    return tokenizer, model


# 计算评估指标
def compute_metrics(eval_preds: EvalPrediction, tokenizer: PreTrainedTokenizer):
    batched_pred_ids, batched_label_ids = eval_preds

    # 初始化指标字典
    metrics_dct = {'rouge-1': [], 'rouge-2': [], 'rouge-l': [], 'bleu-4': []}
    # 计算每个预测的指标
    for pred_ids, label_ids in zip(batched_pred_ids, batched_label_ids):
        # 解码预测和标签
        pred_txt = tokenizer.decode(pred_ids).strip()
        label_txt = tokenizer.decode(label_ids).strip()
        # 分词
        pred_tokens = list(jieba.cut(pred_txt))
        label_tokens = list(jieba.cut(label_txt))
        # 计算ROUGE分数
        rouge = Rouge()
        scores = rouge.get_scores(' '.join(pred_tokens), ' '.join(label_tokens))
        for k, v in scores[0].items():
            metrics_dct[k].append(round(v['f'] * 100, 4))
        # 计算BLEU-4分数
        metrics_dct['bleu-4'].append(
            sentence_bleu(
                [label_tokens],
                pred_tokens,
                smoothing_function=SmoothingFunction().method3,
            )
        )
    # 返回平均指标
    return {k: np.mean(v) for k, v in metrics_dct.items()}


# 主函数
@app.command()
def main(
        data_dir: Annotated[str, typer.Argument(help='')],  # 数据目录
        model_dir: Annotated[  # 模型目录
            str,
            typer.Argument(
                help='A string that specifies the model id of a pretrained model configuration hosted on huggingface.co, or a path to a directory containing a model configuration file.'
            ),
        ],
        config_file: Annotated[str, typer.Argument(help='')],  # 配置文件
        auto_resume_from_checkpoint: str = typer.Argument(  # 自动恢复检查点
            default='',
            help='If entered as yes, automatically use the latest save checkpoint. If it is a numerical example 12 15, use the corresponding save checkpoint. If the input is no, restart training'
        ),

):
    # 加载微调配置
    ft_config = FinetuningConfig.from_file(config_file)
    # 加载分词器和模型
    tokenizer, model = load_tokenizer_and_model(model_dir, peft_config=ft_config.peft_config)
    # 创建数据管理器
    data_manager = DataManager(data_dir, ft_config.data_config)

    # 获取训练数据集
    train_dataset = data_manager.get_dataset(
        Split.TRAIN,
        functools.partial(
            process_batch,
            tokenizer=tokenizer,
            max_input_length=ft_config.max_input_length,
            max_output_length=ft_config.max_output_length,
        ),
        batched=True,
    )
    print('train_dataset:', train_dataset)
    # 获取验证数据集
    val_dataset = data_manager.get_dataset(
        Split.VALIDATION,
        functools.partial(
            process_batch_eval,
            tokenizer=tokenizer,
            max_input_length=ft_config.max_input_length,
            max_output_length=ft_config.max_output_length,
        ),
        batched=True,
    )
    if val_dataset is not None:
        print('val_dataset:', val_dataset)
    # 获取测试数据集
    test_dataset = data_manager.get_dataset(
        Split.TEST,
        functools.partial(
            process_batch_eval,
            tokenizer=tokenizer,
            max_input_length=ft_config.max_input_length,
            max_output_length=ft_config.max_output_length,
        ),
        batched=True,
    )
    if test_dataset is not None:
        print('test_dataset:', test_dataset)

    # 检查编码后的数据集
    _sanity_check(
        train_dataset[0]["input_ids"], train_dataset[0]["labels"], tokenizer
    )

    # 将模型转换为fp32
    _prepare_model_for_training(model, ft_config.training_args.use_cpu)

    # 设置生成配置
    ft_config.training_args.generation_config.pad_token_id = (
        tokenizer.pad_token_id
    )
    ft_config.training_args.generation_config.eos_token_id = [
        tokenizer.eos_token_id,
        tokenizer.get_command('<|user|>'),
        tokenizer.get_command('<|observation|>'),
    ]
    # 启用梯度检查点
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()

    # 创建训练器
    trainer = Seq2SeqTrainer(
        model=model,
        args=ft_config.training_args,
        data_collator=DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            padding='longest',
            return_tensors='pt',
        ),
        train_dataset=train_dataset,
        eval_dataset=val_dataset.select(list(range(50))),
        tokenizer=tokenizer if ft_config.peft_config.peft_type != "LORA" else None,  # LORA不需要分词器
        compute_metrics=functools.partial(compute_metrics, tokenizer=tokenizer),#计算指标compute_metrics函数自己写
    )

    # 处理检查点恢复
    if auto_resume_from_checkpoint.upper() == "" or auto_resume_from_checkpoint is None:
        # 直接开始训练
        trainer.train()
    else:
        # 获取输出目录
        output_dir = ft_config.training_args.output_dir
        dirlist = os.listdir(output_dir)
        checkpoint_sn = 0
        # 查找最新的检查点
        for checkpoint_str in dirlist:
            if checkpoint_str.find("eckpoint") > 0 and checkpoint_str.find("tmp") == -1 and not checkpoint_str.startswith('.'):
                checkpoint = int(checkpoint_str.replace("checkpoint-", ""))
                if checkpoint > checkpoint_sn:
                    checkpoint_sn = checkpoint
        # 如果设置为自动恢复
        if auto_resume_from_checkpoint.upper() == "YES":
            if checkpoint_sn > 0:
                # 启用梯度检查点
                model.gradient_checkpointing_enable()
                model.enable_input_require_grads()
                # 从检查点恢复
                checkpoint_directory = os.path.join(output_dir, "checkpoint-" + str(checkpoint_sn))
                print("resume checkpoint from  checkpoint-" + str(checkpoint_sn))
                trainer.train(resume_from_checkpoint=checkpoint_directory)
            else:
                # 没有检查点，直接训练
                trainer.train()
        else:
            # 如果指定了检查点编号
            if auto_resume_from_checkpoint.isdigit():
                if int(auto_resume_from_checkpoint) > 0:
                    checkpoint_sn = int(auto_resume_from_checkpoint)
                    # 启用梯度检查点
                    model.gradient_checkpointing_enable()
                    model.enable_input_require_grads()
                    # 从指定检查点恢复
                    checkpoint_directory = os.path.join(output_dir, "checkpoint-" + str(checkpoint_sn))
                    print("resume checkpoint from  checkpoint-" + str(checkpoint_sn))
                    trainer.train(resume_from_checkpoint=checkpoint_directory)
            else:
                # 指定的检查点不存在
                print(auto_resume_from_checkpoint,
                      "The specified checkpoint sn(" + auto_resume_from_checkpoint + ") has not been saved. Please search for the correct chkeckpoint in the model output directory")

    # 测试阶段
    if test_dataset is not None:
        trainer.predict(test_dataset)


# 程序入口点
if __name__ == '__main__':
    app()
