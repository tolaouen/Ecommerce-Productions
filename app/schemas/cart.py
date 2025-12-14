from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)

class CartItem(CartItemBase):
    pass

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    updated_at: datetime
    
    class Config:
        from_attributes = True