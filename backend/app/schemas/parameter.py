from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ParameterListItem(BaseModel):
    """参数列表项响应"""
    id: int
    material_category: str
    param_name: str
    param_definition: Optional[str] = None
    test_standard: Optional[str] = None
    standard_unit: Optional[str] = None
    is_core: bool = False
    view_count: int = 0
    favorite_count: int = 0

    class Config:
        from_attributes = True


class ParameterResponse(BaseModel):
    """参数详情响应"""
    id: int
    material_category: str
    param_name: str
    param_definition: Optional[str] = None
    test_standard: Optional[str] = None
    standard_unit: Optional[str] = None
    user_focus: Optional[str] = None
    marking_spec: Optional[str] = None
    remark: Optional[str] = None
    is_core: bool = False
    standard_value: Optional[str] = None
    view_count: int = 0
    favorite_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ParameterSearch(BaseModel):
    """参数搜索响应项"""
    id: int
    param_name: str
    material_category: str
    param_definition: Optional[str] = None
    highlight: Optional[str] = None

    class Config:
        from_attributes = True


class MaterialCategory(str, Enum):
    FIBERGLASS = "玻纤板(FR-4/G11)"
    PI_BOARD = "PI板"
    SPECIAL_PLASTIC = "特种塑胶通用(PEEK/PPS/PEI/电木)"


class CategoryResponse(BaseModel):
    """材料分类响应"""
    value: str
    label: str
    count: int
