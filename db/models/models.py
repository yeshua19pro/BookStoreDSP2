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

class Review(Base):
    __tablename__ = "reviews" # Table name in the database
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Primary key with UUID
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    book_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    commentary: Mapped[str] = mapped_column(String(1000), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    
