### 2.1 HDFS的使用

启动之前需要先修改IP地址！！！（根据课堂笔记的步骤）

- 启动HDFS(在任何路径)

  ```shell
  [hadoop@hadoop00 ]$ start-all.sh
  ```
  - 可以看到 namenode和 datanode启动的日志信息

  ```shell
  Starting namenodes on [hadoop00]
  hadoop00: starting namenode, logging to /home/hadoop/app/hadoop-2.6.0-cdh5.7.0/logs/hadoop-hadoop-namenode-hadoop00.out
  localhost: starting datanode, logging to /home/hadoop/app/hadoop-2.6.0-cdh5.7.0/logs/hadoop-hadoop-datanode-hadoop00.out
  Starting secondary namenodes [0.0.0.0]
  0.0.0.0: starting secondarynamenode, logging to /home/hadoop/app/hadoop-2.6.0-cdh5.7.0/logs/hadoop-hadoop-secondarynamenode-hadoop00.out
  ```
  - 通过jps命令查看当前运行的进程（必须有5个进程才算启动成功）

  ```shell
  [hadoop@hadoop00 sbin]$ jps
  10736 Jps
  5235 NameNode
  6694 NodeManager
  5624 DataNode
  6299 ResourceManager
  6108 SecondaryNameNode
  ```
  - 可以看到 NameNode DataNode 以及 SecondaryNameNode 说明启动成功
- 通过可视化界面查看HDFS的运行情况

  - 通过浏览器查看 主机ip:50070端口

  ![1551174774098](/img/hadoop-state.png)

  - Overview界面查看整体情况

  ![1551174978741](/img/hadoop-state1.png)

  - Datanodes界面查看datanode的情况

    ![1551175081051](/img/hadoop-state2.png)
