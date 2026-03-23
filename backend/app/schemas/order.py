from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    """创建订单请求"""
    order_type: str = Field(..., description="订单类型：template|consultation|vip_membership")
    item_id: Optional[int] = Field(None, description="模板ID或咨询ID（VIP会员无需item_id）")
    item_name: Optional[str] = Field(None, max_length=200, description="项目名称（可选，后端自动填充）")


class OrderResponse(BaseModel):
    """订单详情响应"""
    id: int
    order_no: str
    order_type: str
    item_id: Optional[int] = None
    item_name: str
    amount: float
    status: str = "pending"
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderPayRequest(BaseModel):
    """发起支付请求"""
    payment_method: str = Field(default="wechat", description="支付方式")


class OrderPayResponse(BaseModel):
    """支付响应"""
    payment_params: dict = Field(..., description="微信支付参数")
