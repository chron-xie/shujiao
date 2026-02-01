from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.consultation import Consultation
from app.schemas.consultation import (
    ConsultationCreate,
    ConsultationUpdate,
    ConsultationInDB,
)

router = APIRouter()


@router.post("/", response_model=ConsultationInDB)
async def create_consultation(
    consultation_in: ConsultationCreate,
    user_id: int = 1,  # TODO: 从JWT token中获取
    db: AsyncSession = Depends(get_db),
):
    """创建咨询预约"""
    consultation = Consultation(**consultation_in.model_dump(), user_id=user_id)
    db.add(consultation)
    await db.commit()
    await db.refresh(consultation)
    return consultation


@router.get("/my", response_model=List[ConsultationInDB])
async def get_my_consultations(
    user_id: int = 1,  # TODO: 从JWT token中获取
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """获取我的咨询预约列表"""
    query = (
        select(Consultation)
        .where(Consultation.user_id == user_id)
        .order_by(Consultation.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    consultations = result.scalars().all()
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationInDB)
async def get_consultation(consultation_id: int, db: AsyncSession = Depends(get_db)):
    """获取咨询详情"""
    result = await db.execute(
        select(Consultation).where(Consultation.id == consultation_id)
    )
    consultation = result.scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="咨询记录不存在")

    return consultation


@router.put("/{consultation_id}", response_model=ConsultationInDB)
async def update_consultation(
    consultation_id: int,
    consultation_in: ConsultationUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新咨询状态（管理员功能）"""
    result = await db.execute(
        select(Consultation).where(Consultation.id == consultation_id)
    )
    consultation = result.scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="咨询记录不存在")

    update_data = consultation_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(consultation, field, value)

    await db.commit()
    await db.refresh(consultation)
    return consultation
