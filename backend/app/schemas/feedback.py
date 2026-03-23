from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FeedbackCreate(BaseModel):
    """提交反馈请求"""
    feedback_type: str = Field(..., description="反馈类型：功能建议|问题反馈|内容纠错|其他")
    content: str = Field(..., min_length=10, max_length=1000, description="反馈内容")
    contact: Optional[str] = Field(None, max_length=100, description="联系方式（可选）")
    images: Optional[List[str]] = Field(None, description="截图URL列表（可选）")


class FeedbackResponse(BaseModel):
    """反馈详情响应"""
    id: int
    feedback_type: str
    content: str
    contact: Optional[str] = None
    images: Optional[List[str]] = None
    status: str = "pending"
    admin_reply: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
