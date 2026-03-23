"""显示所有表"""
import pymysql

conn = pymysql.connect(
    host='47.116.114.44',
    port=3306,
    user='root',
    password='A123456z',
    database='shujiao'
)

try:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("=== 数据库中的表 ===")
        for table in tables:
            print(table[0])
finally:
    conn.close()
