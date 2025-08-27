-- 创建一个商品goods数据表
create table goods(
    id int unsigned primary key auto_increment not null,
    name varchar(150) not null,
    cate_name varchar(40) not null,
    brand_name varchar(40) not null,
    price decimal(10,3) not null default 0,
    is_show bit not null default 1,
    is_saleoff bit not null default 0
);

-- 向goods表中插入数据

insert into goods values(0,'r510vc 15.6英寸笔记本','笔记本','华硕','3399',default,default);
insert into goods values(0,'y400n 14.0英寸笔记本电脑','笔记本','联想','4999',default,default);
insert into goods values(0,'g150th 15.6英寸游戏本','游戏本','雷神','8499',default,default);
insert into goods values(0,'x550cc 15.6英寸笔记本','笔记本','华硕','2799',default,default);
insert into goods values(0,'x240 超极本','超级本','联想','4880',default,default);
insert into goods values(0,'u330p 13.3英寸超极本','超级本','联想','4299',default,default);
insert into goods values(0,'svp13226scb 触控超极本','超级本','索尼','7999',default,default);
insert into goods values(0,'ipad mini 7.9英寸平板电脑','平板电脑','苹果','1998',default,default);
insert into goods values(0,'ipad air 9.7英寸平板电脑','平板电脑','苹果','3388',default,default);
insert into goods values(0,'ipad mini 配备 retina 显示屏','平板电脑','苹果','2788',default,default);
insert into goods values(0,'ideacentre c340 20英寸一体电脑 ','台式机','联想','3499',default,default);
insert into goods values(0,'vostro 3800-r1206 台式电脑','台式机','戴尔','2899',default,default);
insert into goods values(0,'imac me086ch/a 21.5英寸一体电脑','台式机','苹果','9188',default,default);
insert into goods values(0,'at7-7414lp 台式电脑 linux ）','台式机','宏碁','3699',default,default);
insert into goods values(0,'z220sff f4f06pa工作站','服务器/工作站','惠普','4288',default,default);
insert into goods values(0,'poweredge ii服务器','服务器/工作站','戴尔','5388',default,default);
insert into goods values(0,'mac pro专业级台式电脑','服务器/工作站','苹果','28888',default,default);
insert into goods values(0,'hmz-t3w 头戴显示设备','笔记本配件','索尼','6999',default,default);
insert into goods values(0,'商务双肩背包','笔记本配件','索尼','99',default,default);
insert into goods values(0,'x3250 m4机架式服务器','服务器/工作站','ibm','6888',default,default);
insert into goods values(0,'商务双肩背包','笔记本配件','索尼','99',default,default);


# •将goods cate_name分组结果写入到goods_cates数据表
-- 创建goods_cates表
create table goods_cates(
    id int unsigned primary key auto_increment not null,
    name varchar(40) not null
);

-- 将goods表中的分类名称数据提取出来，并去重，插入到goods_cates表中
insert into goods_cates(name) 
select distinct cate_name from goods;

-- 查看goods_cates表中的数据
select * from goods_cates;


# •将goods brand_name分组结果写入到goods_brands数据表
-- 创建goods_brands表
create table goods_brands(
    id int unsigned primary key auto_increment not null,
    name varchar(40) not null
) select distinct brand_name as name from goods;


-- 查看goods_brands表中的数据
select * from goods_brands;


-- 通过goods_brands数据表来更新goods数据表中的brand_name,把其变为id
update goods g inner join goods_brands b on g.brand_name = b.name set g.brand_name = b.id;

-- 通过goods_cates数据表来更新goods数据表中的cate_name,把其变为id
update goods g inner join goods_cates c on g.cate_name = c.name set g.cate_name = c.id;

-- •通过alter table语句修改goods表结构
alter table goods  
change cate_name cate_id int unsigned not null,
change brand_name brand_id int unsigned not null;

# goods关联goods_cates和goods_brands进行内连接查询
-- 使用内连接查询goods表与goods_cates和goods_brands表的关联数据
select g.id, g.name, c.name as cate_name, b.name as brand_name, g.price 
from goods as g
inner join goods_cates as c on g.cate_id = c.id
inner join goods_brands as b on g.brand_id = b.id;


# 给goods表增加外键，关联goods_brands和goods_cates
-- 给goods表增加外键，关联goods_cates表
alter table goods
add constraint fk_goods_cates
foreign key (cate_id) references goods_cates(id);

-- 给goods表增加外键，关联goods_brands表
alter table goods
add constraint fk_goods_brands
foreign key (brand_id) references goods_brands(id);

-- 往goods表中插入数据,是一台联想打印机
insert into goods values(0,'联想打印机',8,2,'1099',default,default);

-- 往goods_cates表中插入数据,是 打印机
insert into goods_cates values(0,'打印机');


alter table goods drop foreign key fk_goods_brands;

-- -----------------------练习多对多--------------------------------
#创建teacher表，里边有id，name
create table teacher(
    id int unsigned primary key auto_increment not null,
    name varchar(20) not null
);

insert into teacher values(1,'math teacher');
insert into teacher values(2,'chinese teacher');
insert into teacher values(3,'english teacher');

#创建student表，里边有id，name
create table student(
    id int unsigned primary key auto_increment not null,
    name varchar(20) not null
);

insert into student values(1,'lily');
insert into student values(2,'lucy');
insert into student values(3,'lilei');
insert into student values(4,'xiongda');

#创建teacher_student表，用于多对多关联
create table teacher_student(
    t_id int unsigned not null,
    s_id int unsigned not null,
    primary key (t_id, s_id),
    foreign key (t_id) references teacher(id),
    foreign key (s_id) references student(id)
);

#插入一些测试数据
insert into teacher_student values(1, 1);
insert into teacher_student values(1, 2);
insert into teacher_student values(2, 1);
insert into teacher_student values(2, 3);
insert into teacher_student values(3, 2);
insert into teacher_student values(3, 4);


-- 查询什么老师教什么学生
select t.name as '老师', s.name as '学生'
from teacher t
inner join teacher_student ts on t.id = ts.t_id
inner join student s on s.id = ts.s_id
order by t.id, s.id;
