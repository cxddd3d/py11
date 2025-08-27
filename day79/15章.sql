-- 删除学生表，班级表
drop table if exists students;
drop table if exists classes;

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

-- 向students表中插入数据
INSERT INTO students(name, age, height, gender, cls_id, is_delete)
VALUES ('小明', 18, 180.00, 2, 1, 0),
       ('小月月', 18, 180.00, 2, 2, 1),
       ('彭于晏', 29, 185.00, 1, 1, 0),
       ('刘德华', 59, 175.00, 1, 2, 1),
       ('黄蓉', 38, 160.00, 2, 1, 0),
       ('凤姐', 28, 150.00, 4, 2, 1),
       ('王祖贤', 18, 172.00, 2, 1, 1),
       ('周杰伦', 36, NULL, 1, 1, 0),
       ('程坤', 27, 181.00, 1, 2, 0),
       ('刘亦菲', 25, 166.00, 2, 2, 0),
       ('金星', 33, 162.00, 3, 3, 1),
       ('静香', 12, 180.00, 2, 4, 0),
       ('郭靖', 12, 170.00, 1, 4, 0),
       ('周杰', 34, 176.00, 2, 5, 0);

-- 向classes表中插入数据
insert into classes
values (0, 'python_01期'),
       (0, 'python_02期');

-- 查询学生姓名
select name, age
from students;

# •使用 as 给字段起别名
select id as 序号, name as 名字, gender as 性别
from students;

# •消除重复行
select distinct gender
from students;

# 例1：查询编号大于3的学生
select *
from students
where id > 3;

# 例3：查询姓名不是“黄蓉”的学生
select *
from students
where name != '黄蓉';

# 例5：查询编号大于3的女同学
select *
from students
where id > 3
  and gender = 2;

# 例6：查询编号小于4或没被删除的学生
select *
from students
where id < 4
   or is_delete = 0;

-- 模糊查询
# 例7：查询姓黄的学生
select *
from students
where name like '小%';

# 例9：查询姓黄或靖结尾的学生
select *
from students
where name like '黄%'
   or name like '%靖';

# 例10：查询编号是1或3或8的学生
select *
from students
where id in (1, 3, 8);

# 例11：查询编号为3至8的学生
select *
from students
where id between 3 and 8;

# 例12：查询编号是3至8的男生
select *
from students
where gender = 1
  and id between 3 and 8;

-- 空判断
select *
from students
where height is null;

# 例15：查询填写了身高的男生
select *
from students
where height is not null
  and gender = 1;

# 增加一条记录，name是luke，age是38，height是180.00，gender是1，cls_id是1
insert into students(name, age, height, gender, cls_id)
values ('luke', 38, 180.00, 1, 1);

# 查询姓名是LUKE的学生的信息,注意大小写
select *
from students
where binary name = 'luke';

# 例1：查询未删除男生信息，按学号降序
select *
from students
where is_delete = 0
  and gender = 1
order by id desc;

# 例3：显示所有的学生信息，先按照年龄从大-->小排序，当年龄相同时 按照身高从低到高排序
select *
from students
order by age desc, height asc;

-- ---------------------------聚合函数----------------------------------
# 例1：查询学生总数
select count(*)
from students;

# 使用max，min，avg，sum等聚合函数
select max(age)
from students;
select min(age)
from students;
select avg(age)
from students;

#对平均年龄取整,round取整是四舍五入
select round(avg(age))
from students;

# 对平均年龄向上取整
select ceil(avg(age))
from students;

# 对平均年龄向下取整
select floor(avg(age))
from students;

select sum(age)
from students;

-- ---------------------------分组查询----------------------------------
# 求不同性别的平均年龄
select gender, avg(age)
from students
group by gender;

# 把不同性别的姓名放到一起
select gender, group_concat(name)
from students
group by gender;

select gender, group_concat(id)
from students
group by gender;

# 分别统计性别为男/女的人的个数
select gender, count(*)
from students
group by gender;

# 按性别分组，组内人数大于2的人
select gender, count(*)
from students
group by gender
having count(*) > 2;

# 分别统计性别为男/女的人的个数,再使用rollup函数
select gender, count(*)
from students
group by gender
with rollup;


-- ---------------------------窗口函数----------------------------------
# rank()作用是给出排名，但是遇到相同的分数，保留所有相同的排名
# dense_rank()作用是给出排名，但是遇到相同的分数，保留一个排名
# row_number()作用是给出排名，但是遇到相同的分数，保留所有相同的排名，但是排名不连续
select *,
       rank() over (partition by cls_id order by age desc)       as rank1,
       dense_rank() over (partition by cls_id order by age desc) as dese_rank,
       row_number() over (partition by cls_id order by age desc) as row_num
from students;

-- ---------------------------获取部分行--------------------------------------------------------------------
# 例1：查询前3行男生信息
select * from students where gender = 1 limit 0,3;


# •求第n页的数据，每页5条
select * from students limit 10,5;


-- ---------------------------多表查询--------------------------------------------------------------
# 学生表和班级表进行内连接
select * from students inner join classes on students.cls_id = classes.id;

# 学生表和班级表进行左连接
select * from students left join classes on students.cls_id = classes.id;

# 学生表和班级表进行右连接,班级表放在左边
select * from classes right join students on students.cls_id = classes.id;


-- ---------------------------自关联--------------------------------------------------------------
create table areas(
    aid int primary key,
    atitle varchar(50),
    pid int
);

# 统计areas行数
select count(*) from areas;

# •例1：查询省的名称为“山西省”的所有城市
select city.aid, city.atitle, province.atitle
from areas as city
inner join areas as province on city.pid = province.aid
where province.atitle = '山西省';

#•例2：查询市的名称为“广州市”的所有区县
select district.aid, district.atitle, city.atitle,city.aid
from areas district
inner join areas city on district.pid = city.aid
where city.atitle = '广州市';

