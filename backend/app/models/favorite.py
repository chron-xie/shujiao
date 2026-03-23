from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class UserFavorite(Base, TimestampMixin):
    __tablename__ = "user_favorites"

    id = Column(Integer, primary_key=True, index=True, comment="收藏ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    favorite_type = Column(String(20), nullable=False, comment="收藏类型：parameter|template")
    item_id = Column(Integer, nullable=False, comment="项目ID（参数ID或模板ID）")

    # 关系
    user = relationship("User", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint('user_id', 'favorite_type', 'item_id', name='uk_user_favorite'),
        Index('idx_user_type', 'user_id', 'favorite_type'),
    )
