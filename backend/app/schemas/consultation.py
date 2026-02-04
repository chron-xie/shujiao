from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ConsultationCreate(BaseModel):
    """创建咨询预约请求"""
    name: str = Field(..., max_length=100, description="姓名/称呼")
    company: Optional[str] = Field(None, max_length=200, description="公司/店铺名称（可选）")
    consult_type: str = Field(..., description="咨询类型")
    problem: str = Field(..., min_length=50, max_length=500, description="问题描述（至少50字）")
    contact: str = Field(..., max_length=100, description="联系方式（微信/电话）")

    @validator('problem')
    def validate_problem_length(cls, v):
        if len(v) < 50:
            raise ValueError('问题描述至少50字')
        return v


class ConsultationResponse(BaseModel):
    """咨询详情响应"""
    id: int
    name: str
    company: Optional[str] = None
    consult_type: str
    problem: str
    contact: str
    status: str = "待沟通"
    price: float = 99.00
    consultation_time: Optional[datetime] = None
    summary: Optional[str] = None
    actions: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConsultationListItem(BaseModel):
    """咨询列表项响应"""
    id: int
    consult_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConsultationUpdate(BaseModel):
    """更新咨询状态请求（管理员）"""
    status: Optional[str] = None
    consultation_time: Optional[datetime] = None
    summary: Optional[str] = None
    actions: Optional[List[str]] = None
    admin_notes: Optional[str] = None


class ConsultationBatchUpdate(BaseModel):
    """批量更新咨询状态请求"""
    consultation_ids: List[int] = Field(..., description="咨询ID列表")
    status: str = Field(..., description="新状态: 待沟通/已完成/已取消")


class ConsultationInDB(BaseModel):
    """数据库中的咨询记录"""
    id: int
    user_id: int
    name: str
    company: Optional[str] = None
    consult_type: str
    problem: str
    contact: str
    status: str = "待沟通"
    price: float = 99.00
    consultation_time: Optional[datetime] = None
    summary: Optional[str] = None
    actions: Optional[List[str]] = None
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
