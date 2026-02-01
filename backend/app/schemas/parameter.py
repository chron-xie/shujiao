from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.parameter import MaterialCategory


class ParameterBase(BaseModel):
    material_category: MaterialCategory
    param_name: str
    param_definition: Optional[str] = None
    test_standard: Optional[str] = None
    standard_unit: Optional[str] = None
    user_focus: Optional[str] = None
    marking_spec: Optional[str] = None
    remark: Optional[str] = None
    is_core: int = 0
    sort_order: int = 0


class ParameterCreate(ParameterBase):
    pass


class ParameterUpdate(BaseModel):
    material_category: Optional[MaterialCategory] = None
    param_name: Optional[str] = None
    param_definition: Optional[str] = None
    test_standard: Optional[str] = None
    standard_unit: Optional[str] = None
    user_focus: Optional[str] = None
    marking_spec: Optional[str] = None
    remark: Optional[str] = None
    is_core: Optional[int] = None
    sort_order: Optional[int] = None


class ParameterInDB(ParameterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ParameterListResponse(BaseModel):
    id: int
    material_category: MaterialCategory
    param_name: str
    standard_unit: Optional[str]
    is_core: int

    class Config:
        from_attributes = True
