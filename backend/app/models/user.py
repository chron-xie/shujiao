from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True, nullable=False, comment="微信openid")
    nickname = Column(String(100), comment="微信昵称")
    avatar_url = Column(String(500), comment="头像URL")
    phone = Column(String(20), comment="手机号")
    is_active = Column(Boolean, default=True, comment="是否激活")
