from fastapi import APIRouter, HTTPException, Depends, Request, status # Constructor for router, request for ip directions
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession # Engine for postgress async
from models.catalog_service_models import (BookInfo, FilterBooks, RegisterBook) # Validation models for auth (Account creation, login, token response)       
from services.catalog_service import register_book, create_access_token, filter_book # Auxiliar functions for routers
from core.security import validate_token 
from db.session import get_session # Get async session for bd
from db.models.models import Book # Structure of the table
from core.limiter import limiter
from sqlalchemy.future import select # Select for queries
from uuid import UUID , uuid4 # UUID for tables ids
from datetime import datetime, timedelta, timezone # Time management
import random 
from utils.time import utc_now, utc_return_time_cast # Router functions for lesser verbouse text

router = APIRouter(prefix="/catalog", tags=["Catalogs"]) # All endpoints will start with /catalog and tagged as Catalogs

@router.post("/register-book", status_code = status.HTTP_201_CREATED, include_in_schema=True) 
@limiter.limit("2/minute")
async def register_book_router (
    registry_data: RegisterBook, # Pseudo model for book registration form
    request: Request,
    token_data: dict = Depends(validate_token),
    db: AsyncSession = Depends(get_session) # Async session for bd
    ):
    """Endpoint to register a new book."""

    if not token_data.get("role") == "admin":
        return JSONResponse(
            status_code = status.HTTP_403_FORBIDDEN,
            content={"detail":"You do not have permission to perform this action."}
        )
        
    book = await register_book(db, registry_data)
    
    if not book:
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content={"detail":"book with this name already exists."}
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content={"detail":"book registered successfully."}
    )
    
@router.post("/filter_book", response_model=BookInfo, include_in_schema=True)
@limiter.limit("20/minute")
async def filter_book_router ( # Pseudo model for book validation
    filter_data: FilterBooks,
    request: Request,
    db: AsyncSession = Depends(get_session), # Async session for bd
    token_data: str = Depends(validate_token) # if token no valid, logout. If valid, the session will be extended
    ):
    """Endpoint to login an book."""

    books = await filter_book(db, filter_data)
    
    if not books:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail":"Books Not found."}
        )
    token = create_access_token({ #recreate token for the user to refresh session
        'sub': token_data.get('sub'),
        'role': token_data.get('role'),
        'name': token_data.get('name'),
        'last_name': token_data.get('last_name') or None
    })
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content={"access_token":token, "token_type":"bearer", "book_info": books} # based on the bookinfor model.
    )