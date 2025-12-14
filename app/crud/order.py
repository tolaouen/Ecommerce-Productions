from sqlalchemy.orm import Session
from typing import List
from app.models.order import Order
from app.schemas.order import OrderCreate

def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).all()

def create_order(db: Session, user_id: str, items: List[dict], total_amount: float):
    db_order = Order(
        user_id=user_id,
        items=items,
        total_amount=total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def concel_order(db: Session, user_id):
    db_order = db.query(Order).filter(Order.user_id == user_id).first()

    db.delete(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order
