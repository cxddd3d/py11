create view goods_view as
(
select goods.id as id, goods.name as name, goods_cates.name as type
from goods
         left outer join goods_cates on goods_cates.id = goods.cate_id);