## spark-core实战

课程目标

- 独立实现spark standalone模式的启动

**启动Spark集群**

- 进入到$SPARK_HOME/sbin目录

  - 启动Master

  ```shell
  ./start-master.sh -h 192.168.19.137
  ```
  - 启动Slave

  ```shell
   ./start-slave.sh spark://192.168.19.137:7077
  ```
  - jps查看进程

  ```shell
  27073 Master
  27151 Worker
  ```
  - 关闭防火墙

  ```shell
  systemctl stop firewalld
  ```
  - 通过SPARK WEB UI查看Spark集群及Spark
    - http://192.168.19.137:8080/  监控Spark集群
