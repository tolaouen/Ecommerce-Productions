from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import Relationship
from datetime import datetime
from app.database import Base

class Role(Base):
    __tablename__ = "role"

    id = Column(String, primary_key=True)
    name = Column(String(80), unique=True, default=None, nullable=False)
    description = Column(String(120), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    Permission = Relationship("Permission", back_populates="user", selist=False)



