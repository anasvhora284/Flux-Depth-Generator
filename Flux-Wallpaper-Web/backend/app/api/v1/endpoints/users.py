from typing import Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.core import security
from app.schemas.user import UserResponse

router = APIRouter()

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None

class Toggle2FA(BaseModel):
    enable: bool

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user profile.
    """
    if user_in.full_name:
        current_user.full_name = user_in.full_name
    if user_in.email:
        # Check uniqueness if changing email
        if user_in.email != current_user.email:
             result = await db.execute(select(User).filter(User.email == user_in.email))
             existing = result.scalars().first()
             if existing:
                 raise HTTPException(status_code=400, detail="Email already taken")
             current_user.email = user_in.email
    if user_in.password:
        current_user.hashed_password = security.get_password_hash(user_in.password)
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/2fa")
async def toggle_2fa(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: Toggle2FA,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Enable or Disable 2FA.
    """
    current_user.is_2fa_enabled = data.enable
    db.add(current_user)
    await db.commit()
    return {"message": f"2FA {'enabled' if data.enable else 'disabled'}"}
