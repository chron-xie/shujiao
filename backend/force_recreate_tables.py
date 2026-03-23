"""强制删除并重新创建所有表"""
import pymysql

# 连接数据库
conn = pymysql.connect(
    host='47.116.114.44',
    port=3306,
    user='root',
    password='A123456z',
    database='shujiao'
)

try:
    with conn.cursor() as cursor:
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("=== 删除所有现有表 ===")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            table_name = table[0]
            print(f"删除表: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        conn.commit()
        print("✅ 所有表已删除")

finally:
    conn.close()

print("\n现在运行SQLAlchemy创建表...")
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings
# 导入所有模型，让SQLAlchemy知道要创建哪些表
from app import models

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 新表创建完成")

asyncio.run(create_all_tables())
