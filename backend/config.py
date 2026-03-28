from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(default="postgresql+asyncpg://vpn_user:vpn_password@localhost:5432/vpn_db")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # Security
    secret_key: str = Field(default="your-secret-key-here")
    fernet_key: str = Field(default="")
    algorithm: str = Field(default="HS256")
    
    # API
    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)
    backend_debug: bool = Field(default=False)
    
    # WG Manager
    wg_manager_host: str = Field(default="localhost")
    wg_manager_port: int = Field(default=8001)
    wg_manager_secret: str = Field(default="wg-manager-secret")
    
    # Telegram
    telegram_bot_token: Optional[str] = Field(default=None)
    telegram_api_hash: Optional[str] = Field(default=None)
    telegram_app_id: Optional[int] = Field(default=None)
    
    # Features
    trial_days: int = Field(default=7)
    weekly_price: int = Field(default=50)
    monthly_price: int = Field(default=150)
    max_devices_per_user: int = Field(default=3)
    subscription_check_interval: int = Field(default=300)  # 5 minutes
    notification_hours_before: int = Field(default=24)
    
    # Logging
    log_level: str = Field(default="INFO")
    sentry_dsn: Optional[str] = Field(default=None)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
