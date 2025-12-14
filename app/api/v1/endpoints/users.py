from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, User
from app.crud.user import create_user, get_user, update_user, delete_user, get_all_user
from app.api.deps import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=User)
def get_user_endpoint(user_id: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=List[User])
def get_all_user_endpoint(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_all_user(db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="All user not found"
        )
    
    return user

@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: str, user: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Users can only update their own profile unless they're admin
    if user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Users can only delete their own account unless they're admin
    if user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted_user