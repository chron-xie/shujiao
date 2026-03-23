"""
删除并重新创建数据库表
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def recreate_tables():
    """删除并重新创建所有表"""
    async with engine.begin() as conn:
        # 先删除所有表
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ 旧表已删除")

        # 重新创建所有表
        await conn.run_sync(Base.metadata.create_all)
        print("✅ 新表已创建")


async def main():
    """主函数"""
    print("🚀 开始重新创建数据库表...")
    print("⚠️  警告：此操作将删除所有现有数据！")

    try:
        await recreate_tables()
        print("\n✅ 数据库表重新创建完成！")
    except Exception as e:
        print(f"\n❌ 操作失败：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
