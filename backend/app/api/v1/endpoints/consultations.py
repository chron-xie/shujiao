from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.session import get_db
from app.models.consultation import Consultation
from app.schemas.consultation import (
    ConsultationCreate,
    ConsultationUpdate,
    ConsultationBatchUpdate,
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


@router.get("/admin/list", response_model=List[ConsultationInDB])
async def get_all_consultations_admin(
    status: Optional[str] = Query(None, description="筛选状态: 待沟通/已完成/已取消"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """管理员获取所有咨询列表（支持状态筛选）"""
    query = select(Consultation).order_by(Consultation.created_at.desc())

    if status:
        query = query.where(Consultation.status == status)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    consultations = result.scalars().all()
    return consultations


@router.put("/admin/batch-update")
async def batch_update_consultations(
    data: ConsultationBatchUpdate,
    db: AsyncSession = Depends(get_db),
):
    """批量更新咨询状态（管理员）"""
    # Validate status
    valid_statuses = ["待沟通", "已完成", "已取消"]
    if data.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"无效的状态值，必须是: {', '.join(valid_statuses)}"
        )

    # Fetch consultations
    result = await db.execute(
        select(Consultation).where(Consultation.id.in_(data.consultation_ids))
    )
    consultations = result.scalars().all()

    if not consultations:
        raise HTTPException(status_code=404, detail="未找到咨询记录")

    # Update status
    for consultation in consultations:
        consultation.status = data.status

    await db.commit()

    return {
        "success": True,
        "updated_count": len(consultations),
        "status": data.status
    }
