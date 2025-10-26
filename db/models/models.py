from sqlalchemy.orm import Mapped, mapped_column, relationship # object relational mapping, relationships between tables, tracking, consistency
from sqlalchemy import String, Integer, Float,  TIMESTAMP, func, ForeignKey,Index, CheckConstraint, Enum, Boolean  
from sqlalchemy.dialects.postgresql import UUID # specialized types for postgresql
import uuid 
from .base import Base # to know that all models inherit from base
from datetime import datetime 
from typing import Optional # Option 'T' in rust
from sqlalchemy.dialects.postgresql import JSONB # special type for amongodb like json
import enum
from typing import Dict, Any # dictionaries and any data type
from sqlalchemy.ext.mutable import MutableDict # to track changes in jsonb columns
from datetime import datetime, timedelta 

class User(Base):
    __tablename__ = "users" # Table name in the database

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4) # Primary key with UUID is created automatically
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable = False) # User email, unique and not null
    hashed_password: Mapped[str] = mapped_column(String(255), nullable = False) # Hashed password, not null
    name: Mapped[str] = mapped_column(String(100), nullable=False) # User's first name, not null
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable = True) # User's last name, optional
    address: Mapped[str] = mapped_column(String(255), nullable = False) # User's address, not null
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True), server_default = func.now(), nullable=False) # Account creation date, defaults to now
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True), server_default = func.now(), onupdate=func.now(), nullable=False) # Last login date, updates on login
    role: Mapped[str] = mapped_column(String(50), nullable = False, default="user") # User role, defaults to 'user'