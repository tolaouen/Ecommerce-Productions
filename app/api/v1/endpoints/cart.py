from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.cart import Cart, CartItem
from app.api.deps import get_current_user
from app.database import get_db
from app.crud import cart as crud_cart
from app.crud import product as crud_product

router = APIRouter()

@router.get("", response_model=Cart)
def get_cart(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = crud_cart.get_cart(db, user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/items", response_model=Cart)
def add_to_cart(
    item: CartItem,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id=item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    return crud_cart.add_to_cart(db, user_id=current_user.id, item=item)

@router.delete("/items/{product_id}", response_model=Cart)
def remove_from_cart(
    product_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_cart.remove_from_cart(db, user_id=current_user.id, product_id=product_id)

@router.delete("", response_model=Cart)
def clear_cart(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_cart.clear_cart(db, user_id=current_user.id)