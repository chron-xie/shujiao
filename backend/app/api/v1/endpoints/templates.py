from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.session import get_db
from app.models.template import Template, TemplateCategory
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateInDB,
    TemplateListResponse,
)

router = APIRouter()


@router.get("/", response_model=List[TemplateListResponse])
async def get_templates(
    template_category: Optional[TemplateCategory] = None,
    is_free: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    获取模板列表
    - template_category: 模板分类筛选
    - is_free: 是否免费筛选
    """
    query = select(Template).order_by(Template.sort_order.desc(), Template.created_at.desc())

    if template_category:
        query = query.where(Template.template_category == template_category)

    if is_free is not None:
        query = query.where(Template.is_free == is_free)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    templates = result.scalars().all()

    return templates


@router.get("/{template_id}", response_model=TemplateInDB)
async def get_template(template_id: int, db: AsyncSession = Depends(get_db)):
    """获取模板详情"""
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    return template


@router.post("/", response_model=TemplateInDB)
async def create_template(
    template_in: TemplateCreate, db: AsyncSession = Depends(get_db)
):
    """创建模板（管理员功能）"""
    template = Template(**template_in.model_dump())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.put("/{template_id}", response_model=TemplateInDB)
async def update_template(
    template_id: int, template_in: TemplateUpdate, db: AsyncSession = Depends(get_db)
):
    """更新模板（管理员功能）"""
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    update_data = template_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.commit()
    await db.refresh(template)
    return template


@router.delete("/{template_id}")
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    """删除模板（管理员功能）"""
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    await db.delete(template)
    await db.commit()
    return {"message": "删除成功"}


@router.post("/{template_id}/download")
async def record_download(template_id: int, db: AsyncSession = Depends(get_db)):
    """记录模板下载次数"""
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    template.download_count += 1
    await db.commit()
    return {"message": "下载记录成功", "download_count": template.download_count}
