from pydantic import BaseModel, Field
from typing import Optional

class BookCreate(BaseModel):
    """
    用於 POST 與 PUT 的請求模型。
    所有欄位皆為可選，但price 則必須大於 0。
    """
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    # price 必須大於 0。
    price: int = Field(..., gt=0, description="價格必須大於 0") 
    publish_date: Optional[str] = None
    isbn: Optional[str] = None
    cover_url: Optional[str] = None


class BookResponse(BaseModel):
    """
    用於 API 回傳的模型，包含資料庫生成 id 與 created_at。
    """
    id: int
    title: str
    author: str
    publisher: Optional[str] = None
    price: int
    publish_date: Optional[str] = None
    isbn: Optional[str] = None
    cover_url: Optional[str] = None
    created_at: str  # SQLite 的 TIMESTAMP