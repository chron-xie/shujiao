from sqlalchemy import Column, Integer, String, Text, Enum
import enum
from app.db.base import Base, TimestampMixin


class MaterialCategory(str, enum.Enum):
    """材料分类"""
    FR4_G11 = "玻纤板(FR-4/G11)"
    PI = "PI板"
    SPECIAL_PLASTIC = "特种塑胶通用"


class Parameter(Base, TimestampMixin):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    material_category = Column(Enum(MaterialCategory), nullable=False, index=True, comment="材料分类")
    param_name = Column(String(100), nullable=False, index=True, comment="参数名称")
    param_definition = Column(Text, comment="参数定义")
    test_standard = Column(String(200), comment="测试标准")
    standard_unit = Column(String(50), comment="标准单位")
    user_focus = Column(Text, comment="客户关注点")
    marking_spec = Column(Text, comment="标注规范")
    remark = Column(Text, comment="备注")
    is_core = Column(Integer, default=0, comment="是否核心参数 0-否 1-是")
    sort_order = Column(Integer, default=0, comment="排序权重")
