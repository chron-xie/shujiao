from sqlalchemy import Column, Integer, String, Enum, Numeric, DateTime
import enum
from app.db.base import Base, TimestampMixin


class OrderType(str, enum.Enum):
    """订单类型"""
    TEMPLATE = "template"
    CONSULTATION = "consultation"
    MEMBERSHIP = "membership"


class OrderStatus(str, enum.Enum):
    """订单状态"""
    PENDING = "待支付"
    PAID = "已支付"
    CANCELLED = "已取消"
    REFUNDED = "已退款"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    order_type = Column(Enum(OrderType), nullable=False, comment="订单类型")
    item_id = Column(Integer, comment="商品ID(模板ID/咨询ID)")
    item_name = Column(String(200), comment="商品名称")
    amount = Column(Numeric(10, 2), nullable=False, comment="订单金额")
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, comment="订单状态")
    paid_at = Column(DateTime, comment="支付时间")
    transaction_id = Column(String(100), comment="微信交易号")
