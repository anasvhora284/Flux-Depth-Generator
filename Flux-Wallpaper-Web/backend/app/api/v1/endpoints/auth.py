import random
import string
from datetime import datetime, timedelta
from typing import Any, Optional
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.email import email_service

router = APIRouter()

# Schema for Verification
class OTPVerify(BaseModel):
    email: str
    otp: str

# Helper to generate OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

@router.post("/signup", response_model=UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user with OTP verification.
    """
    # Check if user exists
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    otp = generate_otp()
    otp_expires = datetime.utcnow() + timedelta(minutes=10)

    # Send OTP Email
    await email_service.send_email(
        subject="Verify your Flux Depth account",
        recipients=[user_in.email],
        body=f"""
        <html>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2 style="color: #3b82f6;">Welcome to Flux Depth!</h2>
            <p>Your verification code is:</p>
            <h1 style="font-size: 32px; letter-spacing: 4px; color: #1e293b;">{otp}</h1>
            <p>This code expires in 10 minutes.</p>
            <p style="color: #64748b; font-size: 12px;">If you didn't create this account, you can ignore this email.</p>
        </body>
        </html>
        """
    )
    
    # Create user
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_verified=False, # Wait for OTP
        otp_code=otp,
        otp_expires_at=otp_expires
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/verify-signup", response_model=Token)
async def verify_signup(
    *,
    db: AsyncSession = Depends(deps.get_db),
    verification: OTPVerify,
) -> Any:
    """
    Verify signup OTP and activate user.
    """
    result = await db.execute(select(User).filter(User.email == verification.email))
    user = result.scalars().first()
    
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
         
    if not user.otp_code or user.otp_code != verification.otp:
         raise HTTPException(status_code=400, detail="Invalid OTP")
         
    if datetime.utcnow() > user.otp_expires_at:
         raise HTTPException(status_code=400, detail="OTP Expired")
         
    # Activate
    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    db.add(user)
    await db.commit()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

class ResendOTPRequest(BaseModel):
    email: str

@router.post("/resend-otp")
async def resend_otp(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request: ResendOTPRequest,
) -> Any:
    """
    Resend OTP for unverified users.
    """
    result = await db.execute(select(User).filter(User.email == request.email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    
    # Generate new OTP
    otp = generate_otp()
    otp_expires = datetime.utcnow() + timedelta(minutes=10)
    
    user.otp_code = otp
    user.otp_expires_at = otp_expires
    db.add(user)
    await db.commit()
    
    # Send OTP Email
    await email_service.send_email(
        subject="Flux Depth - New Verification Code",
        recipients=[user.email],
        body=f"""
        <html>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2 style="color: #3b82f6;">New Verification Code</h2>
            <p>Your new verification code is:</p>
            <h1 style="font-size: 32px; letter-spacing: 4px; color: #1e293b;">{otp}</h1>
            <p>This code expires in 10 minutes.</p>
        </body>
        </html>
        """
    )
    
    return {"message": "OTP resent successfully"}


@router.post("/login")
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login. Handles 2FA.
    """
    # Authenticate
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Please verify your email before logging in")

    # 2FA Check
    if user.is_2fa_enabled:
         otp = generate_otp()
         otp_expires = datetime.utcnow() + timedelta(minutes=10)
         
         user.otp_code = otp
         user.otp_expires_at = otp_expires
         db.add(user)
         await db.commit()
         
         # Send 2FA Email
         await email_service.send_email(
             subject="Flux Depth - Your Login Code",
             recipients=[user.email],
             body=f"""
             <html>
             <body style="font-family: sans-serif; padding: 20px;">
                 <h2 style="color: #3b82f6;">Two-Factor Authentication</h2>
                 <p>Your login verification code is:</p>
                 <h1 style="font-size: 32px; letter-spacing: 4px; color: #1e293b;">{otp}</h1>
                 <p>This code expires in 10 minutes.</p>
                 <p style="color: #64748b; font-size: 12px;">If you didn't request this code, please secure your account.</p>
             </body>
             </html>
             """
         )
         
         return {
             "message": "2FA_REQUIRED",
             "detail": "OTP sent to email"
         }

    # Normal Login
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/verify-2fa", response_model=Token)
async def verify_2fa_login(
    *,
    db: AsyncSession = Depends(deps.get_db),
    verification: OTPVerify,
) -> Any:
    """
    Verify 2FA OTP and return token.
    """
    result = await db.execute(select(User).filter(User.email == verification.email))
    user = result.scalars().first()
    
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
         
    if not user.otp_code or user.otp_code != verification.otp:
         raise HTTPException(status_code=400, detail="Invalid OTP")
         
    if datetime.utcnow() > user.otp_expires_at:
         raise HTTPException(status_code=400, detail="OTP Expired")
    
    # Clear OTP
    user.otp_code = None
    user.otp_expires_at = None
    db.add(user)
    await db.commit()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
