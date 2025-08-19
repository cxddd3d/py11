## spark 入门

课程目标：

- 了解spark概念
- 知道spark的特点（与hadoop对比）
- 独立实现spark local模式的启动

### 1.1 spark概述（2014年发布）

- 1、什么是spark

  - **基于内存的计算引擎，它的计算速度非常快。但是仅仅只涉及到数据的计算，并没有涉及到数据的存储。**
- 2、为什么要学习spark

  **MapReduce框架局限性**

  - 1，Map结果写磁盘，Reduce写HDFS，多个MR之间通过HDFS交换数据
  - 2，任务调度和启动开销大
  - 3，无法充分利用内存
  - 4，不适合迭代计算（如机器学习、图计算等等），交互式处理（数据挖掘）
  - 5，不适合流式处理（点击日志分析）
  - 6，MapReduce编程不够灵活，仅支持Map和Reduce两种操作

  **Hadoop生态圈**

  - 批处理：*MapReduce、**Hive （大数据分析）***（spark core spark sql  ）**
  - 流式计算：Storm  （**spark streaming**）
  - 交互式计算：Impala、presto（**spark sql**）  方便学习

  需要一种灵活的框架可同时进行批处理、流式计算、交互式计算

  - 内存计算引擎，提供cache机制来支持需要反复迭代计算或者多次数据共享，减少数据读取的IO开销
  - DAG引擎，减少多次计算之间中间结果写到HDFS的开销
  - 使用多线程模型来减少task启动开销，shuffle过程中避免不必要的sort操作以及减少磁盘IO

  spark的缺点是：**吃内存，不太稳定**
- 3、spark特点

  - 1、速度快（比mapreduce在内存中快100倍，在磁盘中快10倍）
    - spark中的job中间结果可以不落地，可以存放在内存中。
    - mapreduce中map和reduce任务都是以进程的方式运行着，而spark中的job是以线程方式运行在进程中。
  - 2、易用性（可以通过**java**/scala/**python**/R开发spark应用程序）
  - 3、通用性（可以使用spark sql/spark streaming/mlib/Graphx）
  - 4、兼容性（spark程序可以运行在standalone/yarn/mesos）

### 1.2 spark启动（local模式）和WordCount(演示)

- 启动pyspark（注意一定要先启动hadoop）

  - 在$SPARK_HOME/bin目录下执行

    - ./pyspark
  - ![](./img/pyspark.png)
  - ```python
    sc = spark.sparkContext
    words = sc.textFile('file:///root/hadoop_code/words') \
                .flatMap(lambda line: line.split(" ")) \
                .map(lambda x: (x, 1)) \
                .reduceByKey(lambda a, b: a + b).collect()
    ```
  - 输出结果：

    ```shell
    [('world', 1), ('i', 2), ('like', 2), ('java', 1), ('python', 1), ('hello', 1), ('too', 1)]

    ```

可以看出通过spark我们可以快速得到结果，比mapreduce的速度要快很多
