from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TemplateListItem(BaseModel):
    """模板列表项响应"""
    id: int
    template_category: str
    template_name: str
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    price: float = 0.00
    is_free: bool = True
    download_count: int = 0
    view_count: int = 0

    class Config:
        from_attributes = True


class TemplateResponse(BaseModel):
    """模板详情响应"""
    id: int
    template_category: str
    template_name: str
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    price: float = 0.00
    is_free: bool = True
    download_count: int = 0
    purchase_count: int = 0
    view_count: int = 0
    created_at: datetime
    can_download: bool = False

    class Config:
        from_attributes = True


class TemplateDownloadResponse(BaseModel):
    """模板下载响应"""
    download_url: str
    template_name: str
    download_id: int


class TemplateCategoryResponse(BaseModel):
    """模板分类响应"""
    value: str
    label: str
    count: int
