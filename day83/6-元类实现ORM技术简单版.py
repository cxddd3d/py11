# 作者: 王道 龙哥
# 2025年08月30日10时32分33秒
# xxx@qq.com

# 定义元类ModelMetaclass，用于实现ORM映射功能
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 创建一个字典用于存储类属性与数据库表字段的映射关系
        mappings = dict()
        # 遍历类的所有属性
        for k, v in attrs.items():
            # 判断属性是否是元组类型，如果是则认为是数据库字段的定义
            if isinstance(v, tuple):
                print('Found mapping: %s ==> %s' % (k, v))
                # 将属性名和对应的数据库字段信息存入mappings字典
                mappings[k] = v

        # 从类属性中删除已经映射到mappings字典中的属性，避免属性重复
        for k in mappings.keys():
            attrs.pop(k)

        # 在类属性中添加特殊属性，用于存储映射信息
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = name  # 假设表名和类名一致，将类名作为表名
        # 调用父类的__new__方法创建并返回类对象
        return type.__new__(cls, name, bases, attrs)


# 定义User类，使用ModelMetaclass作为元类
class User(metaclass=ModelMetaclass):
    # 定义类属性，每个属性对应数据库表中的一个字段
    # 格式为：属性名 = (数据库字段名, 数据库字段类型)
    uid = ('uid', "int unsigned")  # 用户ID字段
    name = ('username', "varchar(30)")  # 用户名字段
    email = ('email', "varchar(30)")  # 邮箱字段
    password = ('password', "varchar(30)")  # 密码字段

    def __init__(self, **kwargs):
        # 初始化方法，接收关键字参数
        for name, value in kwargs.items():
            # 将传入的参数设置为实例属性
            setattr(self, name, value)

    def save(self):
        # 保存方法，用于生成SQL插入语句并执行
        fields = []  # 存储数据库字段名
        args = []    # 存储对应的值
        # 遍历映射字典
        for k, v in self.__mappings__.items():
            fields.append(v[0])  # 添加数据库字段名
            # 获取实例属性的值，如果不存在则为None
            args.append(getattr(self, k, None))

        # 构造SQL插入语句
        # 对字符串类型的值添加引号，数字类型直接转为字符串
        sql = 'insert into %s (%s) values (%s)' % (
        self.__table__, ','.join(fields), ','.join(["'" + i + "'" if isinstance(i, str) else str(i) for i in args]
                                                   ))
        print('SQL: %s' % sql)  # 打印生成的SQL语句


# 创建User实例并设置属性值
u = User(uid=12345, name='Michael', email='test@orm.org', password='my-pwd')
# print(u.__dict__)  # 打印实例的属性字典（已注释）
u.save()  # 调用save方法，生成并打印SQL语句