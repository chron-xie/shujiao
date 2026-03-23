"""
初始化数据库表并录入测试数据
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models import User, Parameter, Template
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 数据库表创建成功")


async def insert_test_data():
    """插入测试数据"""
    async with AsyncSessionLocal() as session:
        # 插入参数测试数据
        parameters = [
            Parameter(
                material_category="玻纤板(FR-4/G11)",
                param_name="玻璃化温度Tg",
                param_definition="材料从玻璃态到高弹态的转变温度，是衡量材料耐热性的重要指标",
                test_standard="IPC-TM-650 2.4.25 (DSC法)",
                standard_unit="℃",
                user_focus="影响焊接耐热性、尺寸稳定性和可靠性，高Tg板材适用于多层板和高可靠性产品",
                marking_spec="标注格式：Tg ≥ 170℃（高Tg）或 Tg ≥ 150℃（中Tg）",
                remark="FR-4标准Tg为130-140℃，高Tg板材≥170℃",
                is_core=True,
                standard_value="130-170℃",
                view_count=1250,
                favorite_count=85
            ),
            Parameter(
                material_category="玻纤板(FR-4/G11)",
                param_name="击穿电压",
                param_definition="材料被击穿时的电压强度，是衡量绝缘性能的核心指标",
                test_standard="IPC-TM-650 2.5.6",
                standard_unit="kV/mm",
                user_focus="绝缘性能核心指标，关系产品安全性",
                marking_spec="标注格式：≥ XX kV/mm",
                is_core=True,
                standard_value="≥40 kV/mm",
                view_count=1100,
                favorite_count=72
            ),
            Parameter(
                material_category="玻纤板(FR-4/G11)",
                param_name="热膨胀系数CTE",
                param_definition="温度变化时材料的膨胀率，影响焊接可靠性",
                test_standard="IPC-TM-650 2.4.24",
                standard_unit="ppm/℃",
                user_focus="影响焊接可靠性，Z轴CTE尤其重要",
                marking_spec="标注X/Y/Z三个方向的CTE值",
                is_core=True,
                standard_value="X/Y: 12-16 ppm/℃, Z: 50-70 ppm/℃",
                view_count=980,
                favorite_count=65
            ),
            Parameter(
                material_category="PI板",
                param_name="介电常数",
                param_definition="材料的介电特性，影响信号传输速度",
                test_standard="IPC-TM-650 2.5.5.5",
                standard_unit="无",
                is_core=True,
                standard_value="3.0-3.5 @ 1MHz",
                view_count=450,
                favorite_count=30
            ),
            Parameter(
                material_category="特种塑胶通用(PEEK/PPS/PEI/电木)",
                param_name="拉伸强度",
                param_definition="材料抵抗拉伸破坏的能力",
                test_standard="ASTM D638",
                standard_unit="MPa",
                is_core=True,
                standard_value="PEEK: 90-100 MPa",
                view_count=680,
                favorite_count=45
            ),
        ]

        session.add_all(parameters)

        # 插入模板测试数据
        templates = [
            Template(
                template_category="参数表模板",
                template_name="FR-4玻纤板参数表标准模板",
                cover_image_url="https://via.placeholder.com/300x200?text=FR-4",
                description="符合IPC标准的FR-4参数表模板，包含所有核心参数",
                price=0.00,
                is_free=True,
                download_url="https://example.com/templates/fr4-template.xlsx",
                download_count=156,
                purchase_count=0,
                view_count=890,
                is_active=True,
                sort_order=100
            ),
            Template(
                template_category="参数表模板",
                template_name="PEEK特种塑胶全参数表模板",
                cover_image_url="https://via.placeholder.com/300x200?text=PEEK",
                description="PEEK材料完整参数表，含热性能、力学性能、电性能",
                price=19.90,
                is_free=False,
                download_url="https://example.com/templates/peek-template.xlsx",
                download_count=89,
                purchase_count=89,
                view_count=560,
                is_active=True,
                sort_order=90
            ),
            Template(
                template_category="店铺架构模板",
                template_name="1688店铺信息架构优化模板",
                cover_image_url="https://via.placeholder.com/300x200?text=1688",
                description="1688店铺信息架构方案，提升转化率",
                price=29.90,
                is_free=False,
                download_url="https://example.com/templates/1688-template.xlsx",
                download_count=45,
                purchase_count=45,
                view_count=320,
                is_active=True,
                sort_order=80
            ),
            Template(
                template_category="实拍SOP模板",
                template_name="工厂实拍标准化流程SOP",
                cover_image_url="https://via.placeholder.com/300x200?text=SOP",
                description="工厂实拍素材规范指导，包含拍摄角度、光线要求等",
                price=9.90,
                is_free=False,
                download_url="https://example.com/templates/photo-sop.pdf",
                download_count=120,
                purchase_count=120,
                view_count=450,
                is_active=True,
                sort_order=70
            ),
            Template(
                template_category="FAQ话术模板",
                template_name="材料参数常见问题FAQ话术库",
                cover_image_url="https://via.placeholder.com/300x200?text=FAQ",
                description="整理了50+常见客户询问话术及标准回复",
                price=0.00,
                is_free=True,
                download_url="https://example.com/templates/faq-template.docx",
                download_count=230,
                purchase_count=0,
                view_count=780,
                is_active=True,
                sort_order=60
            ),
        ]

        session.add_all(templates)

        await session.commit()
        print("✅ 测试数据插入成功")
        print(f"   - 插入 {len(parameters)} 条参数数据")
        print(f"   - 插入 {len(templates)} 条模板数据")


async def main():
    """主函数"""
    print("🚀 开始初始化数据库...")

    try:
        await create_tables()
        await insert_test_data()
        print("\n✅ 数据库初始化完成！")
        print("\n可以通过以下命令启动后端服务器：")
        print("cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ 初始化失败：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
