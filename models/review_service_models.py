"""
Models for catalog service operations such as registration and book retrieval.
Is the way the data comes in and out of the service.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ReviewData(BaseModel):
    commentary: str
    rating: float

    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
