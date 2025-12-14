from sqlalchemy.orm import Session
from app.models.user import User
from app.models.cart import Cart
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_all_user(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create cart for user
    db_cart = Cart(user_id=db_user.id)
    db.add(db_cart)
    db.commit()
    
    return db_user

def update_user(db: Session, user_id: str, user_update: UserUpdate):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Hash password if it's being updated
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user
