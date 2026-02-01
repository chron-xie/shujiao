from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from app.db.session import get_db
from app.models.parameter import Parameter, MaterialCategory
from app.schemas.parameter import (
    ParameterCreate,
    ParameterUpdate,
    ParameterInDB,
    ParameterListResponse,
)

router = APIRouter()


@router.get("/", response_model=List[ParameterListResponse])
async def get_parameters(
    material_category: Optional[MaterialCategory] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    获取参数列表
    - material_category: 材料分类筛选
    - search: 搜索关键词（参数名称）
    """
    query = select(Parameter).order_by(Parameter.is_core.desc(), Parameter.sort_order.desc())

    if material_category:
        query = query.where(Parameter.material_category == material_category)

    if search:
        query = query.where(
            or_(
                Parameter.param_name.contains(search),
                Parameter.param_definition.contains(search),
            )
        )

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    parameters = result.scalars().all()

    return parameters


@router.get("/{parameter_id}", response_model=ParameterInDB)
async def get_parameter(parameter_id: int, db: AsyncSession = Depends(get_db)):
    """获取参数详情"""
    result = await db.execute(select(Parameter).where(Parameter.id == parameter_id))
    parameter = result.scalar_one_or_none()

    if not parameter:
        raise HTTPException(status_code=404, detail="参数不存在")

    return parameter


@router.post("/", response_model=ParameterInDB)
async def create_parameter(
    parameter_in: ParameterCreate, db: AsyncSession = Depends(get_db)
):
    """创建参数（管理员功能）"""
    parameter = Parameter(**parameter_in.model_dump())
    db.add(parameter)
    await db.commit()
    await db.refresh(parameter)
    return parameter


@router.put("/{parameter_id}", response_model=ParameterInDB)
async def update_parameter(
    parameter_id: int,
    parameter_in: ParameterUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新参数（管理员功能）"""
    result = await db.execute(select(Parameter).where(Parameter.id == parameter_id))
    parameter = result.scalar_one_or_none()

    if not parameter:
        raise HTTPException(status_code=404, detail="参数不存在")

    update_data = parameter_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(parameter, field, value)

    await db.commit()
    await db.refresh(parameter)
    return parameter


@router.delete("/{parameter_id}")
async def delete_parameter(parameter_id: int, db: AsyncSession = Depends(get_db)):
    """删除参数（管理员功能）"""
    result = await db.execute(select(Parameter).where(Parameter.id == parameter_id))
    parameter = result.scalar_one_or_none()

    if not parameter:
        raise HTTPException(status_code=404, detail="参数不存在")

    await db.delete(parameter)
    await db.commit()
    return {"message": "删除成功"}
