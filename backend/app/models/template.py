from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Index
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Template(Base, TimestampMixin):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True, comment="模板ID")
    template_category = Column(String(50), nullable=False, index=True, comment="模板分类：参数表模板|店铺架构模板|实拍SOP模板|FAQ话术模板")
    template_name = Column(String(200), nullable=False, comment="模板名称")
    cover_image_url = Column(String(512), nullable=True, comment="封面图片URL")
    description = Column(Text, nullable=True, comment="模板描述")
    price = Column(Float, default=0.00, comment="价格（元）：0.00免费，9.9/19.9/29.9付费")
    is_free = Column(Boolean, default=True, index=True, comment="是否免费")
    download_url = Column(String(512), nullable=True, comment="下载链接（阿里云盘/腾讯微云）")
    download_count = Column(Integer, default=0, comment="下载次数")
    purchase_count = Column(Integer, default=0, comment="购买次数")
    view_count = Column(Integer, default=0, comment="查看次数")
    is_active = Column(Boolean, default=True, comment="是否上架")
    sort_order = Column(Integer, default=0, comment="排序权重（越大越靠前）")

    # 关系
    downloads = relationship("Download", back_populates="template", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_template_filter', 'template_category', 'is_free', 'is_active', 'sort_order'),
    )
