# 作者: 王道 龙哥
# 2025年08月27日10时58分25秒
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
    
    # 定义SQL查询语句 - 查询goods表中id大于4的数据
    sql = "SELECT * FROM goods WHERE id > %s"
    
    # 查询参数
    param = (4,)
    
    # 执行SQL查询
    count=cursor.execute(sql, param)
    # 打印查询结果总数
    print(f"查询到 {count} 条记录:")
    
    #使用for循环逐条获取并打印结果
    for i in range(count):
        row = cursor.fetchone()
        print(f"第{i+1}条记录: {row}")
    # # 获取所有查询结果
    # results = cursor.fetchall()
    #
    # # 打印查询结果
    # print(f"查询到 {len(results)} 条记录:")
    # print(results)
    
except pymysql.Error as e:
    print(f"数据库错误: {e}")
    
finally:
    # 关闭游标和连接
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("数据库连接已关闭")
