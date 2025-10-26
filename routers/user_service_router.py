from fastapi import APIRouter, HTTPException, Depends, Request, status # Constructor for router, request for ip directions
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession # Engine for postgress async
from models.user_service_models import (LoginForm, AuthenticatedUser, TokenResponse, RegisterForm, TokenResponse) # Validation models for auth (Account creation, login, token response)       
from services.user_service import register_user, create_access_token, login_user, verify_password, hash_password, load_user # Auxiliar functions for routers
from core.security import validate_token 
from db.session import get_session # Get async session for bd
from db.models.models import User # Structure of the table
from core.limiter import limiter
from sqlalchemy.future import select # Select for queries
from uuid import UUID , uuid4 # UUID for tables ids
from datetime import datetime, timedelta, timezone # Time management
import random 
from utils.time import utc_now, utc_return_time_cast # Router functions for lesser verbouse text

router = APIRouter(prefix="/users", tags=["Users"]) # All endpoints will start with /users and tagged as Users

@router.post("/register", status_code = status.HTTP_201_CREATED, include_in_schema=True) 
@limiter.limit("5/minute")
async def register_user_router (
    registry_data: RegisterForm, # Pseudo model for user registration fields
    request: Request,
    db: AsyncSession = Depends(get_session) # Async session for bd
    ):
    """Endpoint to register a new user."""

    user = await register_user(db, registry_data)
    
    if not user:
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content={"detail":"User with this email already exists."}
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content={"detail":"User registered successfully."}
    )
    
@router.post("/login", response_model=TokenResponse, include_in_schema=True)
@limiter.limit("5/minute")
async def login_user_router ( # Pseudo model for user validation
    login: LoginForm,
    request: Request,
    db: AsyncSession = Depends(get_session) # Async session for bd
    ):
    """Endpoint to login an user."""

    user = await login_user(db, login.email, login.password)
    
    if not user:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={"detail":"User Not found."}
        )
    token = create_access_token({
        'sub': str(user.id),
        'role': user.role,
        'name': user.name,
        'last_name': user.last_name or None 
    })
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content={"access_token":token, "token_type":"bearer"}
    )
    
@router.post("/me", status_code = status.HTTP_200_OK, response_model = AuthenticatedUser, include_in_schema=True) 
@limiter.limit("60/minute")
async def load_personal_data (
    request: Request,
    token_data: dict = Depends(validate_token),
    db: AsyncSession = Depends(get_session) # Async session for bd       
    ):
    """Endpoint to load the user personal data"""

    user = await load_user(db, token_data.get("sub"))
    
    if not user:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={"detail":"User Not found."}
        )
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content={"user_name":user.name, "user_lastname":user.last_name, "user_last_login":utc_return_time_cast(user.last_login),
                 "user_address":user.address, "user_creation_date":utc_return_time_cast(user.creation_date), "user_role":user.role,
                 "user_email":user.email}
    )