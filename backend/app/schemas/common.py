from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List, Any

T = TypeVar('T')


class ResponseModel(BaseModel):
    """通用响应模型"""
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
