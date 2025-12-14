from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.schemas.cart import CartItem
from datetime import datetime

def get_cart(db: Session, user_id: str):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def add_to_cart(db: Session, user_id: str, item: CartItem):
    cart = get_cart(db, user_id)
    if not cart:
        cart = Cart(user_id=user_id, items=[])
        db.add(cart)
    
    items = cart.items if cart.items else []
    existing_item = next((i for i in items if i["product_id"] == item.product_id), None)
    
    if existing_item:
        existing_item["quantity"] += item.quantity
    else:
        items.append({"product_id": item.product_id, "quantity": item.quantity})
    
    cart.items = items
    cart.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(cart)
    return cart

def remove_from_cart(db: Session, user_id: str, product_id: str):
    cart = get_cart(db, user_id)
    if cart and cart.items:
        cart.items = [i for i in cart.items if i["product_id"] != product_id]
        cart.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(cart)
    return cart

def clear_cart(db: Session, user_id: str):
    cart = get_cart(db, user_id)
    if cart:
        cart.items = []
        cart.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(cart)
    return cart
