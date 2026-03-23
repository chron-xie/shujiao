from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, comment="订单ID")
    order_no = Column(String(32), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    order_type = Column(String(20), nullable=False, comment="订单类型：template|consultation|vip_membership")
    item_id = Column(Integer, nullable=True, comment="关联项目ID（模板ID或咨询ID）")
    item_name = Column(String(200), nullable=False, comment="项目名称")
    amount = Column(Float, nullable=False, comment="订单金额（元）")
    status = Column(String(20), default="pending", comment="订单状态：pending|paid|cancelled|refunded")
    payment_method = Column(String(20), nullable=True, comment="支付方式：wechat")
    transaction_id = Column(String(64), nullable=True, comment="微信支付交易号")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")

    # 关系
    user = relationship("User", back_populates="orders")
    downloads = relationship("Download", back_populates="order")

    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'status', 'created_at'),
    )
