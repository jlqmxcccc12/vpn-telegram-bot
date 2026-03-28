from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Payment, PaymentStatus
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class PaymentRepository:
    """Repository for payment operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, payment_id: int) -> Payment | None:
        """Get payment by ID."""
        return await self.session.get(Payment, payment_id)
    
    async def get_by_telegram_id(self, telegram_payment_id: str) -> Payment | None:
        """Get payment by Telegram payment ID."""
        result = await self.session.execute(
            select(Payment).where(Payment.telegram_payment_id == telegram_payment_id)
        )
        return result.scalars().first()
    
    async def get_user_payments(self, user_id: int) -> list[Payment]:
        """Get all payments for user."""
        result = await self.session.execute(
            select(Payment).where(Payment.user_id == user_id)
        )
        return result.scalars().all()
    
    async def create(
        self,
        user_id: int,
        telegram_payment_id: str,
        amount: int,
        subscription_type: str
    ) -> Payment:
        """Create new payment record."""
        payment = Payment(
            user_id=user_id,
            telegram_payment_id=telegram_payment_id,
            amount=amount,
            subscription_type=subscription_type,
            status=PaymentStatus.PENDING
        )
        self.session.add(payment)
        await self.session.flush()
        logger.info(f"Created payment {payment.id} for user {user_id}")
        return payment
    
    async def update_status(
        self,
        payment_id: int,
        status: PaymentStatus
    ) -> None:
        """Update payment status."""
        payment = await self.get_by_id(payment_id)
        if payment:
            payment.status = status
            await self.session.flush()
            logger.info(f"Updated payment {payment_id} status to {status}")
