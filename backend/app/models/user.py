from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    wechat_openid = Column(String(64), unique=True, index=True, nullable=False, comment="微信OpenID")
    wechat_unionid = Column(String(64), nullable=True, comment="微信UnionID（可选）")
    nickname = Column(String(100), default="微信用户", comment="用户昵称")
    avatar_url = Column(String(512), nullable=True, comment="用户头像URL")
    phone = Column(String(20), nullable=True, comment="手机号")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_vip = Column(Boolean, default=False, comment="是否全库会员")
    vip_expire_at = Column(DateTime, nullable=True, comment="VIP到期时间")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")

    # 关系
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="user", cascade="all, delete-orphan")
    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user")
