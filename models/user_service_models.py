"""
Models for user service operations such as registration and authentication.
Is the way the data comes in and out of the service.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class RegisterForm(BaseModel):
    email: EmailStr
    password: str
    name: str
    last_name: Optional[str] = None
    address: str
    role: str = "user" # default role is user

class AuthenticatedUser(BaseModel):
    id: str # this would be need to be casted in the future, this CAN'T BE HARDCODED AS UUID
    email: EmailStr
    name: str
    last_name: Optional[str] = None
    
class LoginForm(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"