from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models import AdminLogin, TokenResponse, AdminResponse
from ..auth import authenticate_admin, create_access_token, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_database

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: AdminLogin,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Authenticate admin and return access token."""
    try:
        user = await authenticate_admin(db, login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Update last login
        await db.admin_users.update_one(
            {"email": user.email},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, 
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Return in seconds
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=AdminResponse)
async def get_current_user(
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current admin user information."""
    try:
        user_data = await db.admin_users.find_one({"email": admin_email})
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return AdminResponse(**user_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )

@router.post("/logout")
async def logout(admin_email: str = Depends(get_current_admin)):
    """Logout endpoint (client should delete token)."""
    return {"success": True, "message": "Logged out successfully"}

@router.get("/validate-token")
async def validate_token(admin_email: str = Depends(get_current_admin)):
    """Validate if the current token is valid."""
    return {"valid": True, "email": admin_email}