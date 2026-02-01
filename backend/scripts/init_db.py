"""
数据库初始化脚本
创建所有表
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import engine
from app.models import Base


async def init_db():
    """创建所有表"""
    async with engine.begin() as conn:
        # 删除所有表 (开发环境使用，生产环境需要使用Alembic)
        # await conn.run_sync(Base.metadata.drop_all)

        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    print("✅ 数据库表创建成功！")


if __name__ == "__main__":
    asyncio.run(init_db())
