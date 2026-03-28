from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class SubscriptionType(str, Enum):
    TRIAL = "trial"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    trial_used: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    type: SubscriptionType
    start_date: datetime
    end_date: datetime
    is_active: bool
    auto_renewal: bool
    
    class Config:
        from_attributes = True


class DeviceCreate(BaseModel):
    name: str = Field(..., max_length=255)


class DeviceResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class VPNClientResponse(BaseModel):
    id: int
    device_id: int
    server_id: int
    public_key: str
    ip_address: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConfigResponse(BaseModel):
    """WireGuard config file response."""
    content: str
    format: str = "conf"


class PaymentIntent(BaseModel):
    user_id: int
    subscription_type: SubscriptionType
    amount: int


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    subscription_type: SubscriptionType
    status: PaymentStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
