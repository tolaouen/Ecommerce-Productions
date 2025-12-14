from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.cart import CartItem

class OrderBase(BaseModel):
    items: List[CartItem]
    total_amount: float

class OrderCreate(BaseModel):
    pass

class Order(OrderBase):
    id: str
    user_id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True