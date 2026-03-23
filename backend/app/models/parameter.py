from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from app.db.base import Base, TimestampMixin


class Parameter(Base, TimestampMixin):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True, comment="参数ID")
    material_category = Column(String(50), nullable=False, index=True, comment="材料分类：玻纤板(FR-4/G11)|PI板|特种塑胶通用(PEEK/PPS/PEI/电木)")
    param_name = Column(String(200), nullable=False, index=True, comment="参数名称")
    param_definition = Column(Text, nullable=True, comment="参数定义")
    test_standard = Column(String(200), nullable=True, comment="测试标准（如：IPC-TM-650）")
    standard_unit = Column(String(50), nullable=True, comment="标准单位")
    user_focus = Column(String(500), nullable=True, comment="用户关注点")
    marking_spec = Column(Text, nullable=True, comment="标注规范")
    remark = Column(Text, nullable=True, comment="备注")
    is_core = Column(Boolean, default=False, comment="是否核心参数")
    standard_value = Column(String(200), nullable=True, comment="标准值/参考值")
    view_count = Column(Integer, default=0, comment="查看次数")
    favorite_count = Column(Integer, default=0, comment="收藏次数")

    __table_args__ = (
        Index('idx_param_search', 'material_category', 'is_core', 'view_count'),
    )
