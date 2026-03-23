from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, update, desc
from typing import Optional
import asyncio

from app.db.session import get_db
from app.models.parameter import Parameter
from app.schemas import (
    ResponseModel,
    PaginatedResponse,
    ParameterListItem,
    ParameterResponse,
    ParameterSearch,
    CategoryResponse,
)

router = APIRouter()


@router.get("/", response_model=ResponseModel)
async def get_parameters(
    material_category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    is_core: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """获取参数列表"""
    query = select(Parameter)

    if material_category:
        query = query.where(Parameter.material_category == material_category)
    if search:
        query = query.where(
            or_(
                Parameter.param_name.contains(search),
                Parameter.param_definition.contains(search)
            )
        )
    if is_core is not None:
        query = query.where(Parameter.is_core == is_core)

    query = query.order_by(desc(Parameter.is_core), desc(Parameter.view_count))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    parameters = result.scalars().all()

    items = [ParameterListItem.from_orm(p) for p in parameters]

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


@router.get("/search", response_model=ResponseModel)
async def search_parameters(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """搜索参数"""
    query = select(Parameter).where(
        or_(
            Parameter.param_name.contains(q),
            Parameter.param_definition.contains(q)
        )
    ).order_by(desc(Parameter.view_count))

    # 分页
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    parameters = result.scalars().all()

    items = []
    for p in parameters:
        items.append(ParameterSearch(
            id=p.id,
            param_name=p.param_name,
            material_category=p.material_category,
            param_definition=p.param_definition,
            highlight=f"<em>{q}</em>" if q in p.param_name else None
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


@router.get("/categories", response_model=ResponseModel)
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取材料分类"""
    categories = [
        "玻纤板(FR-4/G11)",
        "PI板",
        "特种塑胶通用(PEEK/PPS/PEI/电木)"
    ]

    result_list = []
    for cat in categories:
        count_result = await db.execute(
            select(func.count(Parameter.id)).where(Parameter.material_category == cat)
        )
        count = count_result.scalar()
        result_list.append(CategoryResponse(
            value=cat,
            label=cat,
            count=count or 0
        ))

    return ResponseModel(
        code=0,
        message="success",
        data=[item.dict() for item in result_list]
    )


@router.get("/hot", response_model=ResponseModel)
async def get_hot_parameters(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """获取热门参数"""
    query = select(Parameter).order_by(desc(Parameter.view_count)).limit(limit)
    result = await db.execute(query)
    parameters = result.scalars().all()

    items = [ParameterListItem.from_orm(p) for p in parameters]

    return ResponseModel(
        code=0,
        message="success",
        data=[item.dict() for item in items]
    )


@router.get("/{id}", response_model=ResponseModel)
async def get_parameter(id: int, db: AsyncSession = Depends(get_db)):
    """获取参数详情"""
    result = await db.execute(select(Parameter).where(Parameter.id == id))
    parameter = result.scalar_one_or_none()

    if not parameter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="参数不存在"
        )

    # 异步更新 view_count（不等待结果）
    asyncio.create_task(increment_view_count(id))

    return ResponseModel(
        code=0,
        message="success",
        data=ParameterResponse.from_orm(parameter).dict()
    )


@router.post("/", response_model=ResponseModel)
async def create_parameter(parameter_data: dict, db: AsyncSession = Depends(get_db)):
    """创建参数（管理员功能）"""
    parameter = Parameter(**parameter_data)
    db.add(parameter)
    await db.commit()
    await db.refresh(parameter)

    return ResponseModel(
        code=0,
        message="success",
        data=ParameterResponse.from_orm(parameter).dict()
    )


async def increment_view_count(parameter_id: int):
    """异步更新查看次数"""
    from app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            await db.execute(
                update(Parameter)
                .where(Parameter.id == parameter_id)
                .values(view_count=Parameter.view_count + 1)
            )
            await db.commit()
        except Exception:
            pass
