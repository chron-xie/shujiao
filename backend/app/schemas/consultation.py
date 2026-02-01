from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.consultation import ConsultType, ConsultStatus


class ConsultationBase(BaseModel):
    name: str
    company: Optional[str] = None
    consult_type: ConsultType
    problem: str
    contact: str


class ConsultationCreate(ConsultationBase):
    pass


class ConsultationUpdate(BaseModel):
    status: Optional[ConsultStatus] = None
    order_id: Optional[int] = None


class ConsultationInDB(ConsultationBase):
    id: int
    user_id: int
    status: ConsultStatus
    order_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
