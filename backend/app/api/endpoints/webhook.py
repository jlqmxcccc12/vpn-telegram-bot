from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import PaymentStatus, SubscriptionType
from app.repository.payment_repo import PaymentRepository
from app.repository.user_repo import UserRepository
from app.services.subscription_service import SubscriptionService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/successful_payment")
async def handle_successful_payment(
    user_id: int,
    telegram_payment_id: str,
    subscription_type: str,
    amount: int,
    session: AsyncSession = Depends(get_session)
):
    """Handle successful Telegram Stars payment."""
    payment_repo = PaymentRepository(session)
    user_repo = UserRepository(session)
    
    # Check if payment already processed
    existing = await payment_repo.get_by_telegram_id(telegram_payment_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment already processed"
        )
    
    # Get user
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create payment record
    payment = await payment_repo.create(
        user_id=user_id,
        telegram_payment_id=telegram_payment_id,
        amount=amount,
        subscription_type=subscription_type
    )
    
    # Activate subscription
    sub_service = SubscriptionService(session)
    await sub_service.get_or_create_subscription(
        user,
        SubscriptionType(subscription_type)
    )
    
    # Update payment status
    await payment_repo.update_status(payment.id, PaymentStatus.COMPLETED)
    
    await session.commit()
    logger.info(f"Processed payment {payment.id} for user {user_id}")
    
    return {"message": "Payment processed successfully"}
