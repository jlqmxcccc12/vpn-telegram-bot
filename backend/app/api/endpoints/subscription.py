from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from app.schemas import SubscriptionResponse
from app.repository.subscription_repo import SubscriptionRepository
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get("/user/{user_id}", response_model=SubscriptionResponse | None)
async def get_active_subscription(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get active subscription for user."""
    repo = SubscriptionRepository(session)
    subscription = await repo.get_active_by_user(user_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    return subscription


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get subscription by ID."""
    repo = SubscriptionRepository(session)
    subscription = await repo.get_by_id(subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    return subscription
