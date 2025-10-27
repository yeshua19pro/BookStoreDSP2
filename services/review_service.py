"""
Catalog Service for handling Review-related operations such as Ratting and Comments.
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext # Library for hashing passwords
from jose import jwt # jose. (web tokens)
from datetime import datetime, timezone, timedelta, date # Time management
from sqlalchemy import update, and_ , func # For update queries
from sqlalchemy.ext.asyncio import AsyncSession # Async session for postgress
from sqlalchemy.future import select # Select for queries
from typing import Optional # Similar to 'Option T' in rust
from core.config import settings
from db.models.models import Review # User table structure
from models.review_service_models import ReviewData # own fields for authenticated user
from uuid import UUID, uuid4 # UUID for tables ids
from utils.time import utc_now, utc_return_time_cast
from dateutil import parser
import random
import httpx
# Context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bycrypt algorithm based in SHA 256




def create_access_token(data: dict, expires_minutes: int = 60) -> str: # JWT creation, dictionaries, hashmaps
    """Create a JWT access token for a user."""
    to_encode = data.copy() # deep copy of data to encode
    now = utc_now()
    expires = now + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expires, "iat": now}) # expiration and issued at
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM) # token creation
    return encoded_jwt # token return


async def validate_book_exists(book_id: str):
    params = {
        "x_internal_action_token": settings.INTERNAL_ACTION_TOKEN
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.CATALOG_SERVICE_URL}/catalog/book-exists/{book_id}",
            params=params
        )
    return response.status_code == 200


async def review_book(db: AsyncSession, review_data: ReviewData, book_id : UUID, user_id : UUID):
    """Filter books based on provided criteria."""
    
    check_book_exist = await validate_book_exists(str(book_id))
    
    if not check_book_exist:
        return None
    
    commentary = review_data.commentary
    rating = review_data.rating
    
    new_review = Review(
        user_id=user_id,
        book_id=book_id,
        commentary=commentary,
        rating=rating,
        review_date = utc_now()
    )
    
    db.add(new_review)
    db.commit()
    await db.refresh(new_review)
    return new_review