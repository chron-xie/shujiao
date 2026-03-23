"""检查数据库表结构"""
import asyncio
import pymysql

async def check_schema():
    conn = pymysql.connect(
        host='47.116.114.44',
        port=3306,
        user='root',
        password='A123456z',
        database='shujiao'
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("DESC parameters")
            result = cursor.fetchall()
            print("=== parameters表结构 ===")
            for row in result:
                print(row)
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
