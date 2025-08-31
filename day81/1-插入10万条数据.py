# 作者: 王道 龙哥
# 2025年08月27日10时46分01秒
# xxx@qq.com
import pymysql

# 连接MySQL数据库
try:
    # 建立数据库连接
    conn = pymysql.connect(
        host='192.168.19.128',      # 数据库主机地址
        user='root',           # 数据库用户名
        password='123',     # 数据库密码
        database='py11',       # 数据库名称
        charset='utf8'      # 字符编码
    )
    
    # 创建游标对象
    cursor = conn.cursor()
    
    for i in range(100000):
        # 执行SQL语句
        cursor.execute("insert into test_index values('ha-%s')",(i,))
    
    # 提交事务
    conn.commit()
    

    
except pymysql.Error as e:
    # 发生错误时回滚
    if conn:
        conn.rollback()
    print(f"数据库错误: {e}")
    
finally:
    # 关闭游标和连接
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("数据库连接已关闭")
