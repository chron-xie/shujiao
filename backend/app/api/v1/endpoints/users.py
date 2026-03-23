from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import Optional

from app.db.session import get_db
from app.core.auth import create_access_token, get_current_user
from app.core.wechat import WeChatAPI
from app.models.user import User
from app.models.favorite import UserFavorite
from app.models.parameter import Parameter
from app.models.template import Template
from app.models.order import Order
from app.models.download import Download
from app.schemas import (
    ResponseModel,
    PaginatedResponse,
    UserLogin,
    UserLoginResponse,
    UserResponse,
    UserUpdate,
    FavoriteCreate,
    FavoriteResponse,
    OrderItemResponse,
    DownloadRecordResponse,
)

router = APIRouter()


@router.post("/login", response_model=ResponseModel)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """微信登录"""
    try:
        # 调用微信API获取openid
        wechat_data = await WeChatAPI.code2session(login_data.code)
        openid = wechat_data.get("openid")
        unionid = wechat_data.get("unionid")

        if not openid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="微信登录失败，无法获取openid"
            )

        # 查询用户是否存在
        result = await db.execute(
            select(User).where(User.wechat_openid == openid)
        )
        user = result.scalar_one_or_none()

        # 不存在则创建新用户
        if not user:
            user = User(
                wechat_openid=openid,
                wechat_unionid=unionid,
                nickname="微信用户",
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        await db.commit()

        # 生成JWT token
        access_token = create_access_token(
            data={
                "user_id": user.id,
                "openid": user.wechat_openid,
                "is_vip": user.is_vip,
            }
        )

        return ResponseModel(
            code=0,
            message="success",
            data=UserLoginResponse(
                access_token=access_token,
                token_type="Bearer",
                expires_in=60 * 24 * 7 * 60,  # 7天（秒）
                user=UserResponse.from_orm(user)
            ).dict()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )


@router.get("/me", response_model=ResponseModel)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return ResponseModel(
        code=0,
        message="success",
        data=UserResponse.from_orm(current_user).dict()
    )


@router.put("/me", response_model=ResponseModel)
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return ResponseModel(
        code=0,
        message="success",
        data=UserResponse.from_orm(current_user).dict()
    )


@router.get("/favorites", response_model=ResponseModel)
async def get_favorites(
    favorite_type: Optional[str] = Query(None, description="收藏类型：parameter|template"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取收藏列表"""
    # 构建查询
    query = select(UserFavorite).where(UserFavorite.user_id == current_user.id)

    if favorite_type:
        query = query.where(UserFavorite.favorite_type == favorite_type)

    query = query.order_by(desc(UserFavorite.created_at))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    favorites = result.scalars().all()

    # 获取详情
    items = []
    for fav in favorites:
        detail = None
        if fav.favorite_type == "parameter":
            param_result = await db.execute(
                select(Parameter).where(Parameter.id == fav.item_id)
            )
            param = param_result.scalar_one_or_none()
            if param:
                detail = {
                    "param_name": param.param_name,
                    "material_category": param.material_category,
                    "standard_unit": param.standard_unit,
                }
        elif fav.favorite_type == "template":
            template_result = await db.execute(
                select(Template).where(Template.id == fav.item_id)
            )
            template = template_result.scalar_one_or_none()
            if template:
                detail = {
                    "template_name": template.template_name,
                    "template_category": template.template_category,
                    "price": template.price,
                    "cover_image_url": template.cover_image_url,
                }

        items.append(FavoriteResponse(
            id=fav.id,
            favorite_type=fav.favorite_type,
            item_id=fav.item_id,
            created_at=fav.created_at,
            detail=detail
        ))

    return ResponseModel(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=[item.dict() for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        ).dict()
    )


@router.post("/favorites", response_model=ResponseModel)
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加收藏"""
    # 检查是否已收藏
    result = await db.execute(
        select(UserFavorite).where(
            and_(
                UserFavorite.user_id == current_user.id,
                UserFavorite.favorite_type == favorite_data.favorite_type,
                UserFavorite.item_id == favorite_data.item_id
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已收藏该项目"
        )

    # 创建收藏
    favorite = UserFavorite(
        user_id=current_user.id,
        favorite_type=favorite_data.favorite_type,
        item_id=favorite_data.item_id
    )
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    return ResponseModel(
        code=0,
        message="success",
        data=FavoriteResponse(
            id=favorite.id,
            favorite_type=favorite.favorite_type,
            item_id=favorite.item_id,
            created_at=favorite.created_at
        ).dict()
    )


@router.delete("/favorites/{favorite_id}", response_model=ResponseModel)
async def remove_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏"""
    result = await db.execute(
        select(UserFavorite).where(
            and_(
                UserFavorite.id == favorite_id,
                UserFavorite.user_id == current_user.id
            )
        )
    )
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )

    await db.delete(favorite)
    await db.commit()

    return ResponseModel(code=0, message="success")


@router.get("/orders", response_model=ResponseModel)
async def get_orders(
    order_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取订单列表"""
    query = select(Order).where(Order.user_id == current_user.id)

    if order_type:
        query = query.where(Order.order_type == order_type)
    if status:
        query = query.where(Order.status == status)

    query = query.order_by(desc(Order.created_at))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    orders = result.scalars().all()

    items = [OrderItemResponse.from_orm(order) for order in orders]

    return ResponseModel(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=[item.dict() for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        ).dict()
    )


@router.get("/downloads", response_model=ResponseModel)
async def get_downloads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取下载记录"""
    query = select(Download).where(Download.user_id == current_user.id).order_by(desc(Download.created_at))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    downloads = result.scalars().all()

    # 获取模板详情
    items = []
    for download in downloads:
        template_result = await db.execute(
            select(Template).where(Template.id == download.template_id)
        )
        template = template_result.scalar_one_or_none()

        if template:
            items.append(DownloadRecordResponse(
                id=download.id,
                template_id=download.template_id,
                template_name=template.template_name,
                cover_image_url=template.cover_image_url,
                download_url=download.download_url,
                created_at=download.created_at
            ))

    return ResponseModel(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=[item.dict() for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        ).dict()
    )
