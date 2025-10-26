"""
User service for handling user-related operations such as authentication and registration.
"""
from passlib.context import CryptContext # Library for hashing passwords
from jose import jwt # jose. (web tokens)
from datetime import datetime, timezone, timedelta, date # Time management
from sqlalchemy import update # For update queries
from sqlalchemy.ext.asyncio import AsyncSession # Async session for postgress
from sqlalchemy.future import select # Select for queries
from typing import Optional # Similar to 'Option T' in rust
from core.config import settings
from db.models.models import User # User table structure
from models.user_service_models import AuthenticatedUser, RegisterForm, LoginForm, TokenResponse # own fields for authenticated user
from uuid import UUID, uuid4 # UUID for tables ids
from utils.time import utc_now
import random

# Context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bycrypt algorithm based in SHA 256

def hash_password(password: str) -> str:
    """Hash a plaintext password.""" # Doc string
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password.""" # Doc string
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: int = 60) -> str: # JWT creation, dictionaries, hashmaps
    """Create a JWT access token for a user."""
    to_encode = data.copy() # deep copy of data to encode
    now = utc_now()
    expires = now + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expires, "iat": now}) # expiration and issued at
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM) # token creation
    return encoded_jwt # token return

async def register_user(db: AsyncSession, registry_data: RegisterForm):
    """Register a new user in the database."""
    duplicate_check = await db.execute(select(User).where(User.email == registry_data.email))
    duplicate_check_result = duplicate_check.scalar_one_or_none() # Check if user with this email already exists and return None if not return the user created in memory
    
    if duplicate_check_result:
        return None # User with this email already exists
    new_user = User(
        email = registry_data.email,
        hashed_password = hash_password(registry_data.password),
        name=registry_data.name,
        last_name=registry_data.last_name,
        address=registry_data.address,
        creation_date = utc_now(),
        last_login = utc_now(), #propierties of the user table, are also key sensitive
        role = registry_data.role.strip().lower()
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def login_user(db: AsyncSession, email: str, password: str):
    """Authenticate a user and return the user if successful."""
    check_user_exists = await db.execute(select(User).where(User.email == email)) # SELECT Email, ID, Firstname, Lastname FROM Users WHERE Email =: email
    user = check_user_exists.scalar_one_or_none()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    user.last_login = utc_now()
    await db.commit()
    return user

async def load_user(db: AsyncSession, id: str):
    """Return user data constantly to front end"""
    check_user_exists = await db.execute(select(User).where(User.id == UUID(id))) # SELECT Email, ID, Firstname, Lastname FROM Users WHERE Id =: id casting string to UUID
    user = check_user_exists.scalar_one_or_none()
    
    if not user:
        return None
     
    user.last_login = utc_now()
    await db.commit()
    return user