from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.order import OrderType, OrderStatus


class OrderBase(BaseModel):
    order_type: OrderType
    item_id: Optional[int] = None
    item_name: Optional[str] = None
    amount: Decimal


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    paid_at: Optional[datetime] = None
    transaction_id: Optional[str] = None


class OrderInDB(OrderBase):
    id: int
    order_no: str
    user_id: int
    status: OrderStatus
    paid_at: Optional[datetime]
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
