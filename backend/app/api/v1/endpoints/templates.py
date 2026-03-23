from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from typing import Optional
import asyncio

from app.db.session import get_db
from app.core.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.template import Template
from app.models.download import Download
from app.models.order import Order
from app.schemas import (
    ResponseModel,
    PaginatedResponse,
    TemplateListItem,
    TemplateResponse,
    TemplateDownloadResponse,
    TemplateCategoryResponse,
)

router = APIRouter()


@router.get("/", response_model=ResponseModel)
async def get_templates(
    template_category: Optional[str] = Query(None),
    is_free: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """获取模板列表"""
    query = select(Template).where(Template.is_active == True)

    if template_category:
        query = query.where(Template.template_category == template_category)
    if is_free is not None:
        query = query.where(Template.is_free == is_free)

    query = query.order_by(desc(Template.sort_order), desc(Template.created_at))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    templates = result.scalars().all()

    items = [TemplateListItem.from_orm(t) for t in templates]

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


@router.get("/categories", response_model=ResponseModel)
async def get_template_categories(db: AsyncSession = Depends(get_db)):
    """获取模板分类"""
    categories = [
        "参数表模板",
        "店铺架构模板",
        "实拍SOP模板",
        "FAQ话术模板"
    ]

    result_list = []
    for cat in categories:
        count_result = await db.execute(
            select(func.count(Template.id)).where(
                Template.template_category == cat,
                Template.is_active == True
            )
        )
        count = count_result.scalar()
        result_list.append(TemplateCategoryResponse(
            value=cat,
            label=cat,
            count=count or 0
        ))

    return ResponseModel(
        code=0,
        message="success",
        data=[item.dict() for item in result_list]
    )


@router.get("/{id}", response_model=ResponseModel)
async def get_template(
    id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取模板详情"""
    result = await db.execute(select(Template).where(Template.id == id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在"
        )

    # 判断是否可下载
    can_download = False
    if template.is_free:
        can_download = True
    elif current_user:
        # VIP会员
        if current_user.is_vip:
            can_download = True
        else:
            # 检查是否已购买
            order_result = await db.execute(
                select(Order).where(
                    Order.user_id == current_user.id,
                    Order.order_type == "template",
                    Order.item_id == id,
                    Order.status == "paid"
                )
            )
            if order_result.scalar_one_or_none():
                can_download = True

    # 异步更新view_count
    asyncio.create_task(increment_view_count(id))

    response_data = TemplateResponse.from_orm(template).dict()
    response_data["can_download"] = can_download

    return ResponseModel(
        code=0,
        message="success",
        data=response_data
    )


@router.post("/{id}/download", response_model=ResponseModel)
async def download_template(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """下载模板"""
    result = await db.execute(select(Template).where(Template.id == id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模板不存在"
        )

    # 权限验证
    can_download = False
    order_id = None

    if template.is_free:
        can_download = True
    elif current_user.is_vip:
        can_download = True
    else:
        # 检查是否已购买
        order_result = await db.execute(
            select(Order).where(
                Order.user_id == current_user.id,
                Order.order_type == "template",
                Order.item_id == id,
                Order.status == "paid"
            )
        )
        order = order_result.scalar_one_or_none()
        if order:
            can_download = True
            order_id = order.id

    if not can_download:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要购买后才能下载"
        )

    # 创建下载记录
    download = Download(
        user_id=current_user.id,
        template_id=id,
        order_id=order_id,
        download_url=template.download_url
    )
    db.add(download)

    # 更新下载次数
    template.download_count += 1
    await db.commit()
    await db.refresh(download)

    return ResponseModel(
        code=0,
        message="success",
        data=TemplateDownloadResponse(
            download_url=template.download_url,
            template_name=template.template_name,
            download_id=download.id
        ).dict()
    )


@router.post("/", response_model=ResponseModel)
async def create_template(template_data: dict, db: AsyncSession = Depends(get_db)):
    """创建模板（管理员功能）"""
    template = Template(**template_data)
    db.add(template)
    await db.commit()
    await db.refresh(template)

    return ResponseModel(
        code=0,
        message="success",
        data=TemplateListItem.from_orm(template).dict()
    )


async def increment_view_count(template_id: int):
    """异步更新查看次数"""
    from app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            await db.execute(
                update(Template)
                .where(Template.id == template_id)
                .values(view_count=Template.view_count + 1)
            )
            await db.commit()
        except Exception:
            pass
