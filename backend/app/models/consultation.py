from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Consultation(Base, TimestampMixin):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True, comment="咨询ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    name = Column(String(100), nullable=False, comment="姓名/称呼")
    company = Column(String(200), nullable=True, comment="公司/店铺名称（可选）")
    consult_type = Column(String(100), nullable=False, comment="咨询类型：产品参数梳理与合规标注|1688/淘宝店铺信息架构优化|工厂实拍素材规范指导")
    problem = Column(Text, nullable=False, comment="问题描述（至少50字）")
    contact = Column(String(100), nullable=False, comment="联系方式（微信/电话）")
    status = Column(String(20), default="待沟通", comment="状态：待沟通|已完成|已取消")
    price = Column(Float, default=99.00, comment="咨询费用（元）")
    consultation_time = Column(DateTime, nullable=True, comment="咨询时间")
    summary = Column(Text, nullable=True, comment="咨询总结")
    actions = Column(JSON, nullable=True, comment="可执行动作（JSON格式）")
    admin_notes = Column(Text, nullable=True, comment="管理员备注")

    # 关系
    user = relationship("User", back_populates="consultations")
