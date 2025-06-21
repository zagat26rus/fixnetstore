from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

class RepairStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    DIAGNOSED = "Diagnosed"
    PENDING_PICKUP = "Pending Pickup"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PriorityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class DeviceType(str, Enum):
    IPHONE = "iPhone"
    SAMSUNG = "Samsung"
    GOOGLE = "Google"
    ONEPLUS = "OnePlus"
    OTHER = "Other"

class RepairRequestCreate(BaseModel):
    customerName: str = Field(..., min_length=2, max_length=100)
    customerEmail: EmailStr
    customerPhone: str = Field(..., min_length=10, max_length=20)
    deviceBrand: str = Field(..., min_length=2, max_length=50)
    deviceModel: str = Field(..., min_length=2, max_length=100)
    issueCategory: str = Field(..., min_length=2, max_length=100)
    specificIssue: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    urgency: str = Field(default="normal")
    pickupAddress: str = Field(..., min_length=10, max_length=500)
    pickupTime: Optional[str] = None
    gdprConsent: bool = Field(...)

    @validator('customerPhone')
    def validate_phone(cls, v):
        # Remove all non-digit characters
        phone = re.sub(r'\D', '', v)
        if len(phone) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return v

    @validator('gdprConsent')
    def validate_consent(cls, v):
        if not v:
            raise ValueError('GDPR consent is required')
        return v

class RepairRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticket_id: str = Field(default_factory=lambda: f"FN-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}")
    customerName: str
    customerEmail: EmailStr
    customerPhone: str
    deviceBrand: str
    deviceModel: str
    issueCategory: str
    specificIssue: str
    description: str
    urgency: str
    pickupAddress: str
    pickupTime: Optional[str] = None
    status: RepairStatus = Field(default=RepairStatus.NEW)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    assignedTech: Optional[str] = None
    estimatedCost: Optional[float] = None
    actualCost: Optional[float] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    estimatedCompletion: Optional[datetime] = None
    completedAt: Optional[datetime] = None
    notes: Optional[str] = None
    gdprConsent: bool = True

    class Config:
        use_enum_values = True

class RepairRequestUpdate(BaseModel):
    status: Optional[RepairStatus] = None
    priority: Optional[PriorityLevel] = None
    assignedTech: Optional[str] = None
    estimatedCost: Optional[float] = None
    actualCost: Optional[float] = None
    estimatedCompletion: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        use_enum_values = True

class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class RepairRequestResponse(BaseModel):
    success: bool
    message: str
    ticket_id: str
    data: Optional[RepairRequest] = None

class RepairRequestListResponse(BaseModel):
    success: bool
    total: int
    requests: List[RepairRequest]

class StatusUpdateRequest(BaseModel):
    ticket_id: str
    status: RepairStatus
    notes: Optional[str] = None

    class Config:
        use_enum_values = True

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)