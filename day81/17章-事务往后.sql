use py11;

create table checking(
    id int unsigned primary key auto_increment not null,
    balance int not null
);

insert into checking values(1, 1000);
insert into checking values(2, 0);

-- 学习回滚
begin; # 开始事务
select balance from checking where id=1;
update checking set balance=balance-200 where id=1; # 从账户1中转出200
select balance from checking where id=1;
rollback;
select balance from checking where id=1;
commit; # 提交事务

-- 学习隔离性
begin; # 开始事务
select balance from checking where id=1;
update checking set balance=balance-200 where id=1; # 从账户1中转出200
select balance from checking where id=1;
# 给2号账号加200
update checking set balance=balance+200 where id=2;
select balance from checking where id=2;
commit;

-- ---------------------索引----------------------------------

create table test_index(title varchar(10));

show index from test_index;

select count(*) from test_index;


# 统计时间

# •开启运行时间监测：
set profiling=1;
# •查找第1万条数据ha-99999
select * from test_index where title='ha-99999';
# •查看执行的时间：
show profiles;

# •为表title_index的title列创建索引：
create index title_index on test_index(title(10));
# •执行查询语句：
select * from test_index where title='ha-99999';
# •再次查看执行的时间
show profiles;

show index from test_index;

drop index title_index on test_index;

#查看数据库引擎
show engines;

-- -----------------账户管理--------------------------------------------------------------------
use mysql;


# 查看所有用户
select user, host from user;

# 查看用户权限
show grants for 'root'@'%';

# 创建新用户
# create user '用户名'@'主机名' identified by '密码';
create user 'test'@'localhost' identified by '123456';

# 授予权限
# grant 权限列表 on 数据库.表名 to '用户名'@'主机名';
grant select on py11.* to 'test'@'localhost';

# 查看新用户权限
show grants for 'test'@'localhost';

# 回收权限
# revoke 权限列表 on 数据库.表名 from '用户名'@'主机名';
revoke insert on *.* from 'test'@'localhost';

# 删除用户
# drop user '用户名'@'主机名';
drop user 'test'@'localhost';


-- -----------------主从配置--------------------------------------------------------------------
select uuid();

# 创建数据库t1，编码是utf8
create database t1 character set utf8;

# 下面的192.168.19.129要换为你的从机IP
# 创建一个名为'backup'的用户，允许从IP为192.168.19.129的主机连接，密码设置为'123'
create user 'backup'@'192.168.19.129' identified by '123'; 
# 授予该用户在所有数据库和表上的复制从机权限
GRANT REPLICATION SLAVE ON *.* TO 'backup'@'192.168.19.129';

ALTER USER 'backup'@'192.168.19.129' IDENTIFIED WITH mysql_native_password BY '123';
# 刷新权限表，使权限设置立即生效
flush privileges;

# 查询确认用户权限是不是配好了
# 从mysql.user表中查询用户名、主机名和复制从机权限状态
select user,host,Repl_slave_priv from mysql.user;

# 先创建test数据库，下面注释的部分是要在xshell上进行的
# sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
#
# server-id   = 1
# expire_logs_days = 1
# max_binlog_size   = 100M
# #replicate-do-db=backup1
# #replicate-do-db=backup2
# binlog_do_db = test   #日志产生的是哪个数据库的二进制日志
# binlog_ignore_db  = mysql
# log_bin     = /var/log/mysql/mysql-bin.log
#
# sudo service mysql restart


# 主机看状态
show variables like 'log_%';
# 在主机那边执行
show master status;


# 使用t1数据库
use t1;

# 在t1数据库中创建一个表
create table users (
    id int unsigned primary key auto_increment not null,
    username varchar(50) not null,
    password varchar(100) not null,
    email varchar(100),
    create_time datetime default current_timestamp,
    update_time datetime default current_timestamp on update current_timestamp,
    is_active tinyint(1) default 1
);

# 插入一些测试数据
insert into users (username, password, email) values 
('张三', MD5('password123'), 'zhangsan@example.com'),
('李四', MD5('password456'), 'lisi@example.com'),
('王五', MD5('password789'), 'wangwu@example.com');

# 查看表结构
desc users;

# 查看表数据
select * from users;
