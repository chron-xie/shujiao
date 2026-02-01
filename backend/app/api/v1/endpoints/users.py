from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.models.favorite import Favorite, FavoriteType
from app.schemas.user import UserCreate, UserUpdate, UserInDB

router = APIRouter()


@router.post("/", response_model=UserInDB)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """创建用户（微信登录时）"""
    # 检查用户是否已存在
    result = await db.execute(select(User).where(User.openid == user_in.openid))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return existing_user

    user = User(**user_in.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserInDB)
async def get_current_user(
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user


@router.put("/me", response_model=UserInDB)
async def update_current_user(
    user_in: UserUpdate,
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """更新当前用户信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.post("/favorites")
async def add_favorite(
    favorite_type: FavoriteType,
    favorite_id: int,
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """添加收藏"""
    # 检查是否已收藏
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.favorite_type == favorite_type,
            Favorite.favorite_id == favorite_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        return {"message": "已收藏"}

    favorite = Favorite(
        user_id=user_id, favorite_type=favorite_type, favorite_id=favorite_id
    )
    db.add(favorite)
    await db.commit()
    return {"message": "收藏成功"}


@router.delete("/favorites")
async def remove_favorite(
    favorite_type: FavoriteType,
    favorite_id: int,
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """取消收藏"""
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.favorite_type == favorite_type,
            Favorite.favorite_id == favorite_id,
        )
    )
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(status_code=404, detail="收藏不存在")

    await db.delete(favorite)
    await db.commit()
    return {"message": "取消收藏成功"}


@router.get("/favorites/{favorite_type}")
async def get_favorites(
    favorite_type: FavoriteType,
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """获取收藏列表"""
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id, Favorite.favorite_type == favorite_type)
        .order_by(Favorite.created_at.desc())
    )
    favorites = result.scalars().all()

    # 返回收藏的ID列表
    favorite_ids = [f.favorite_id for f in favorites]
    return {"favorite_ids": favorite_ids, "count": len(favorite_ids)}
