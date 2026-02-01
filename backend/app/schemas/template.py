from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.template import TemplateCategory


class TemplateBase(BaseModel):
    template_category: TemplateCategory
    template_name: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    price: Decimal = Decimal("0.00")
    is_free: bool = False
    download_url: Optional[str] = None
    sort_order: int = 0


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    template_category: Optional[TemplateCategory] = None
    template_name: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    price: Optional[Decimal] = None
    is_free: Optional[bool] = None
    download_url: Optional[str] = None
    sort_order: Optional[int] = None


class TemplateInDB(TemplateBase):
    id: int
    download_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    id: int
    template_category: TemplateCategory
    template_name: str
    cover_image_url: Optional[str]
    price: Decimal
    is_free: bool

    class Config:
        from_attributes = True
