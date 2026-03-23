from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Download(Base, TimestampMixin):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True, comment="下载ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    template_id = Column(Integer, ForeignKey("templates.id", ondelete="CASCADE"), nullable=False, comment="模板ID")
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, comment="关联订单ID（付费模板）")
    download_url = Column(String(512), nullable=False, comment="下载链接")

    # 关系
    user = relationship("User", back_populates="downloads")
    template = relationship("Template", back_populates="downloads")
    order = relationship("Order", back_populates="downloads")

    __table_args__ = (
        Index('idx_user_template', 'user_id', 'template_id'),
    )
