from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.api.deps import get_current_user
from app.database import get_db
from app.crud import product as crud_product

router = APIRouter()

@router.get("", response_model=List[Product])
def get_products(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_product.get_products(db, skip=skip, limit=limit, category=category)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if product with same name already exists
    if crud_product.get_product_by_name(db, name=product_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Product with this name already exists"
        )
    
    return crud_product.create_product(db, product=product_data)



@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = crud_product.update_product(db, product_id=product_id, product_update=product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not crud_product.delete_product(db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")