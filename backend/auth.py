from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from motor.motor_asyncio import AsyncIOMotorDatabase
from .models import AdminUser, AdminResponse

# Security configurations
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fixnet_super_secret_key_change_in_production_2025')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate hash for a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return {"email": email}
    except JWTError:
        return None

async def get_admin_user(db: AsyncIOMotorDatabase, email: str) -> Optional[AdminUser]:
    """Get admin user by email from database."""
    user_data = await db.admin_users.find_one({"email": email})
    if user_data:
        return AdminUser(**user_data)
    return None

async def authenticate_admin(db: AsyncIOMotorDatabase, email: str, password: str) -> Optional[AdminUser]:
    """Authenticate admin user."""
    user = await get_admin_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated admin user."""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["email"]

async def create_default_admin(db: AsyncIOMotorDatabase):
    """Create default admin user if not exists."""
    admin_email = "zagat5654@gmail.com"
    existing_admin = await get_admin_user(db, admin_email)
    
    if not existing_admin:
        hashed_password = get_password_hash("admin123")
        admin_user = AdminUser(
            email=admin_email,
            hashed_password=hashed_password,
            is_active=True
        )
        await db.admin_users.insert_one(admin_user.dict())
        print(f"Created default admin user: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")