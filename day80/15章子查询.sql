use py11;

-- students表
create table students
(
    id        int unsigned primary key auto_increment not null,
    name      varchar(20)                    default '',
    age       tinyint unsigned               default 0,
    height    decimal(5, 2),
    gender    enum ('男','女','中性','保密') default '保密',
    cls_id    int unsigned                   default 0,
    is_delete bit                            default 0
);

-- classes表
create table classes
(
    id   int unsigned auto_increment primary key not null,
    name varchar(30)                             not null
);
# 查询班级哪些学生的身高大于平均身高
select * from students where height >(select avg(height) from students);

# 列子查询
# 查询还有学生在班的所有班级名字
select distinct name from classes
where id in (select cls_id from students);

select max(height),max(age) from students;
select * from students where (height,age) = (select max(height),max(age) from students);