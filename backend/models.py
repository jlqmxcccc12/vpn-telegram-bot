from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

Base = declarative_base()


class SubscriptionType(str, Enum):
    TRIAL = "trial"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), nullable=True, index=True)
    trial_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    type = Column(SQLEnum(SubscriptionType), index=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True, index=True)
    auto_renewal = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="devices")
    vpn_clients = relationship("VPNClient", back_populates="device", cascade="all, delete-orphan")


class Server(Base):
    __tablename__ = "servers"
    
    id = Column(Integer, primary_key=True, index=True)
    host = Column(String(255), unique=True, index=True)
    public_key = Column(String(512))
    endpoint = Column(String(255))
    endpoint_port = Column(Integer, default=51820)
    is_active = Column(Boolean, default=True, index=True)
    max_clients = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    vpn_clients = relationship("VPNClient", back_populates="server", cascade="all, delete-orphan")


class VPNClient(Base):
    __tablename__ = "vpn_clients"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    server_id = Column(Integer, ForeignKey("servers.id"), index=True)
    public_key = Column(String(512), unique=True)
    private_key_encrypted = Column(Text)  # Encrypted with Fernet
    ip_address = Column(String(45), unique=True, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    device = relationship("Device", back_populates="vpn_clients")
    server = relationship("Server", back_populates="vpn_clients")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    telegram_payment_id = Column(String(255), unique=True, index=True)
    amount = Column(Integer)  # In Telegram Stars
    subscription_type = Column(SQLEnum(SubscriptionType))
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="payments")
