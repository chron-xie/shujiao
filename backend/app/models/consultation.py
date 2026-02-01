from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
import enum
from app.db.base import Base, TimestampMixin


class ConsultType(str, enum.Enum):
    """咨询类型"""
    PARAMETER = "参数"
    SHOP = "店铺"
    PHOTO = "实拍"
    OTHER = "其他"


class ConsultStatus(str, enum.Enum):
    """预约状态"""
    PENDING = "待沟通"
    COMPLETED = "已完成"
    CANCELLED = "已取消"


class Consultation(Base, TimestampMixin):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    name = Column(String(50), nullable=False, comment="姓名/称呼")
    company = Column(String(200), comment="公司/店铺名称")
    consult_type = Column(Enum(ConsultType), nullable=False, comment="咨询类型")
    problem = Column(Text, nullable=False, comment="问题描述")
    contact = Column(String(100), nullable=False, comment="联系方式(微信/电话)")
    status = Column(Enum(ConsultStatus), default=ConsultStatus.PENDING, comment="预约状态")
    order_id = Column(Integer, comment="关联订单ID")
