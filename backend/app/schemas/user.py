from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    """微信登录请求"""
    code: str = Field(..., description="微信小程序wx.login()返回的code")


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    nickname: str = "微信用户"
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    is_vip: bool = False
    vip_expire_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """更新用户信息请求"""
    nickname: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)


class UserLoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 604800
    user: UserResponse


class FavoriteCreate(BaseModel):
    """添加收藏请求"""
    favorite_type: str = Field(..., description="收藏类型：parameter|template")
    item_id: int = Field(..., description="项目ID")


class FavoriteResponse(BaseModel):
    """收藏响应"""
    id: int
    favorite_type: str
    item_id: int
    created_at: datetime
    detail: Optional[dict] = None

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    """订单列表项响应"""
    id: int
    order_no: str
    order_type: str
    item_id: Optional[int] = None
    item_name: str
    amount: float
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DownloadRecordResponse(BaseModel):
    """下载记录响应"""
    id: int
    template_id: int
    template_name: str
    cover_image_url: Optional[str] = None
    download_url: str
    created_at: datetime

    class Config:
        from_attributes = True
