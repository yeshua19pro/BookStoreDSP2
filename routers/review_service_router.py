from fastapi import APIRouter, HTTPException, Depends, Request, status # Constructor for router, request for ip directions
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession # Engine for postgress async
from models.review_service_models import ReviewData # Validation models for auth (Account creation, login, token response)       
from services.review_service import review_book, create_access_token # Auxiliar functions for routers
from core.security import validate_token 
from db.session import get_session # Get async session for bd
from core.limiter import limiter
from sqlalchemy.future import select # Select for queries
from uuid import UUID , uuid4 # UUID for tables ids
from datetime import datetime, timedelta, timezone # Time management
import random 
from utils.time import utc_now, utc_return_time_cast # Router functions for lesser verbouse text

router = APIRouter(prefix="/reviews", tags=["Reviews"]) # All endpoints will start with /reviews and tagged as Reviews


@router.post("/review-book/{book_id}", status_code = status.HTTP_201_CREATED, include_in_schema=True) 
@limiter.limit("2/minute")
async def review_book_router (
    book_id: str,
    registry_data: ReviewData, # Pseudo model for review registration form
    request: Request,
    token_data: dict = Depends(validate_token),
    db: AsyncSession = Depends(get_session) # Async session for bd
    ):
    """Endpoint to register a new review."""

    real_book_id = UUID(book_id)
    user_id = UUID(token_data.get("sub"))
    
    
    review = await review_book(db, registry_data, real_book_id, user_id)
    
    if not review:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={"detail":"book with this id not exists."}
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content={"detail":"book registered successfully."}
    )
    
