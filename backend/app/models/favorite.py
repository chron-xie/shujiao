from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
import enum
from app.db.base import Base, TimestampMixin


class FavoriteType(str, enum.Enum):
    """收藏类型"""
    PARAMETER = "parameter"
    TEMPLATE = "template"


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint('user_id', 'favorite_type', 'favorite_id', name='unique_favorite'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    favorite_type = Column(Enum(FavoriteType), nullable=False, comment="收藏类型")
    favorite_id = Column(Integer, nullable=False, comment="收藏目标ID")
