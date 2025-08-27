show databases; -- 显示所有数据库

create database py11 charset utf8; -- 创建数据库; -- 创建数据库

use py11; -- 使用数据库

create database python charset utf8; -- 创建数据库

show create database py11; -- 查看创建数据库的语句

drop database python; -- 删除数据库

show tables; -- 查看当前库的所有表

create table classes(
    id int unsigned auto_increment primary key not null,
    name varchar(20) not null
); -- 创建表

desc classes; -- 查看表结构


create table students(
    id int unsigned primary key auto_increment not null,
    name varchar(20) default '',
    age tinyint unsigned default 0,
    height decimal(5,2),
    gender enum('男','女','保密'),
    cls_id int unsigned default 0
); -- 创建学生表

desc students; -- 查看表结构
-- 给学生表添加birthday字段
alter table students add birthday datetime;

-- 修改students表中birthday字段为birth
alter table students change birthday birth datetime not null;

-- modify birth字段为date类型
alter table students modify birth date not null;

-- 删除birth字段
alter table students drop birth;

-- 创建t1表
create table t1
(
    id   int unsigned primary key auto_increment not null,
    name varchar(20)                             not null
);

-- 删除t1表
drop table t1;

-- 学习增删查改

select * from classes; -- 查看所有班级

insert into classes(name) values('py15'); -- 插入数据
-- 插入数据
insert into students values(0, 'tom', 18, 170.00, '男', 1);

-- 插入数据,理解枚举类型
insert into students(name, height, gender, cls_id) values('tom', 170.00, 2, 1);

select * from students;

-- 向classes表中插入多条数据
insert into classes(name) values('py12'),('py13');

-- 修改id为2的学生的年龄为20
update students set age=20 where id=2;

-- 修改id为2的学生的姓名为tom2,身高为180
update students set name='tom2', height=180 where id=2;


-- 删除id为2的班级
delete from classes where id=2;

-- 添加isdelete字段到students表
alter table students add isdelete bit(1) not null;

-- isdelete字段默认值为0
alter table students change isdelete isdelete bit(1) default 0;

desc students;

insert into students(age, height, gender, cls_id) values(18, 170.00, '男', 1);

-- 插入学生表一条数据，不放身高
insert into students(age, gender, cls_id) values(18, '男', 1);

-- 修改id为4的学生的isdelete为1
update students set isdelete=1 where id=4;

select * from students where isdelete=0;

