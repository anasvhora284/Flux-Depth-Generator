import random
import string
from datetime import datetime, timedelta
from typing import Any, Optional
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
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


# Email Template Helper
def get_email_template(title: str, otp: str, reason: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #000000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #ffffff;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td align="center" style="padding: 40px 0;">
                    <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #0a0a0a; border: 1px solid #333333; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 40px 30px 40px; text-align: center; background: linear-gradient(to right, #1e1e1e, #0a0a0a); border-bottom: 1px solid #333333;">
                                <div style="display: inline-block; padding: 12px; background-color: rgba(255, 255, 255, 0.05); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                                    <h1 style="margin: 0; font-size: 24px; font-weight: 700; background: linear-gradient(90deg, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; color: #60a5fa;">Flux Depth</h1>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px;">
                                <h2 style="margin: 0 0 20px 0; font-size: 24px; font-weight: 600; color: #ffffff; text-align: center;">{title}</h2>
                                
                                <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.6; color: #a1a1aa; text-align: center;">
                                    {reason}
                                </p>
                                
                                <div style="margin: 0 0 30px 0; text-align: center;">
                                    <div style="display: inline-block; padding: 20px 40px; background-color: rgba(99, 102, 241, 0.1); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
                                        <span style="font-family: 'Courier New', monospace; font-size: 32px; font-weight: 700; letter-spacing: 8px; color: #818cf8; display: block;">{otp}</span>
                                    </div>
                                </div>
                                
                                <p style="margin: 0 0 0 0; font-size: 14px; text-align: center; color: #71717a;">
                                    This code will expire in 10 minutes. <br>
                                    If you did not request this, please ignore this email or contact support if you have concerns.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #050505; border-top: 1px solid #333333; text-align: center;">
                                <p style="margin: 0 0 10px 0; font-size: 14px; font-weight: 600; color: #e4e4e7;">Flux Depth Generator</p>
                                <p style="margin: 0 0 20px 0; font-size: 13px; color: #71717a;">
                                    Transforming flat images into immersive 3D realities using advanced AI.
                                    <br>100% Free & Open Source.
                                </p>
                                <p style="margin: 0; font-size: 12px; color: #52525b;">
                                    &copy; {datetime.now().year} Flux Depth. Made with &hearts; by Anas.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

@router.post("/signup", response_model=UserResponse)
async def create_user(
    *,
    background_tasks: BackgroundTasks,
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

    # Queue OTP Email (Background Task)
    background_tasks.add_task(
        email_service.send_email,
        subject="Enable Your Account - Flux Depth",
        recipients=[user_in.email],
        body=get_email_template(
            title="Verify Your Account",
            otp=otp,
            reason="Welcome to Flux Depth! To finish setting up your account and start generating 3D depth maps, please verify your email address using the code below."
        )
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
    background_tasks: BackgroundTasks,
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
    
    # Queue OTP Email (Background Task)
    background_tasks.add_task(
        email_service.send_email,
        subject="New Verification Code - Flux Depth",
        recipients=[user.email],
        body=get_email_template(
            title="New Verification Code",
            otp=otp,
            reason="You requested a new verification code for your Flux Depth account. Please use the code below to verify your email address."
        )
    )
    
    return {"message": "OTP resent successfully"}


@router.post("/login")
async def login_access_token(
    background_tasks: BackgroundTasks,
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
         
         # Queue 2FA Email (Background Task)
         background_tasks.add_task(
             email_service.send_email,
             subject="Login Verification - Flux Depth",
             recipients=[user.email],
             body=get_email_template(
                 title="Two-Factor Authentication",
                 otp=otp,
                 reason="A login attempt was made on your Flux Depth account. Please use the code below to complete the login process."
             )
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

@router.post("/request-password-update-otp")
async def request_password_update_otp(
    *,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Generate and send OTP for password update.
    """
    otp = generate_otp()
    otp_expires = datetime.utcnow() + timedelta(minutes=10)
    
    current_user.otp_code = otp
    current_user.otp_expires_at = otp_expires
    db.add(current_user)
    await db.commit()
    
    background_tasks.add_task(
        email_service.send_email,
        subject="Password Change Verification - Flux Depth",
        recipients=[current_user.email],
        body=get_email_template(
            title="Confirm Password Change",
            otp=otp,
            reason="You requested to change your password for your Flux Depth account. Please use the verification code below to authorize this change."
        )
    )
    
    return {"message": "OTP sent successfully"}
