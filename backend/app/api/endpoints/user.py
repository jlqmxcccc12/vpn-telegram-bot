from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import User
from app.schemas import UserCreate, UserResponse
from app.repository.user_repo import UserRepository
from app.services.subscription_service import SubscriptionService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new user and assign trial subscription."""
    repo = UserRepository(session)
    
    # Check if user already exists
    existing = await repo.get_by_telegram_id(user_create.telegram_id)
    if existing:
        return existing
    
    # Create user
    user = await repo.create(
        telegram_id=user_create.telegram_id,
        username=user_create.username
    )
    
    # Assign trial subscription
    sub_service = SubscriptionService(session)
    trial_activated = await sub_service.get_trial_subscription(user)
    
    if trial_activated:
        logger.info(f"User {user.id} created with trial subscription")
    
    await session.commit()
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get user by ID."""
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram(
    telegram_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get user by Telegram ID."""
    repo = UserRepository(session)
    user = await repo.get_by_telegram_id(telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
