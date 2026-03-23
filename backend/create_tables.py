"""
仅创建数据库表
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def create_tables():
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 数据库表创建成功")


async def main():
    """主函数"""
    print("🚀 开始创建数据库表...")

    try:
        await create_tables()
        print("\n✅ 数据库表创建完成！")
    except Exception as e:
        print(f"\n❌ 创建失败：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
