from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.order import Order
from app.api.deps import get_current_user
from app.database import get_db
from app.crud import order as crud_order
from app.crud import cart as crud_cart
from app.crud import product as crud_product

router = APIRouter()

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = crud_cart.get_cart(db, user_id=current_user.id)
    
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_amount = 0
    for item in cart.items:
        product = crud_product.get_product(db, product_id=item["product_id"])
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")
        if product.stock < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        
        total_amount += product.price * item["quantity"]
        product.stock -= item["quantity"]
    
    db.commit()
    
    order = crud_order.create_order(
        db,
        user_id=current_user.id,
        items=cart.items,
        total_amount=total_amount
    )
    
    crud_cart.clear_cart(db, user_id=current_user.id)
    
    return order

@router.get("/", response_model=List[Order])
def get_orders(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_order.get_user_orders(db, user_id=current_user.id)

@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = crud_order.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

# Cancel order 

@router.delete("/{order_id}", response_model=Order)
def cancel_orders(order_id: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud_order.concel_order(db, order_id=order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    return order