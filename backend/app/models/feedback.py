from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Feedback(Base, TimestampMixin):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, comment="反馈ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="用户ID（可选，支持匿名反馈）")
    feedback_type = Column(String(50), nullable=False, comment="反馈类型：功能建议|问题反馈|内容纠错|其他")
    content = Column(Text, nullable=False, comment="反馈内容")
    contact = Column(String(100), nullable=True, comment="联系方式（可选）")
    images = Column(JSON, nullable=True, comment="截图URL（JSON数组）")
    status = Column(String(20), default="pending", comment="处理状态：pending|processing|resolved|closed")
    admin_reply = Column(Text, nullable=True, comment="管理员回复")

    # 关系
    user = relationship("User", back_populates="feedbacks")
