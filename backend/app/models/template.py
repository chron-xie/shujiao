from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, Boolean
import enum
from app.db.base import Base, TimestampMixin


class TemplateCategory(str, enum.Enum):
    """模板分类"""
    PARAMETER_TABLE = "参数表模板"
    SHOP_STRUCTURE = "店铺架构模板"
    PHOTO_SOP = "实拍SOP模板"
    FAQ_SCRIPT = "FAQ话术模板"


class Template(Base, TimestampMixin):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    template_category = Column(Enum(TemplateCategory), nullable=False, index=True, comment="模板分类")
    template_name = Column(String(200), nullable=False, comment="模板名称")
    description = Column(Text, comment="描述")
    cover_image_url = Column(String(500), comment="封面图URL")
    price = Column(Numeric(10, 2), default=0.00, comment="价格")
    is_free = Column(Boolean, default=False, index=True, comment="是否免费")
    download_url = Column(String(500), comment="下载链接")
    download_count = Column(Integer, default=0, comment="下载次数")
    sort_order = Column(Integer, default=0, comment="排序权重")
