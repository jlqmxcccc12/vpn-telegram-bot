from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from models import Subscription, SubscriptionType
from datetime import datetime, timedelta
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SubscriptionRepository:
    """Repository for subscription operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_active_by_user(self, user_id: int) -> Subscription | None:
        """Get active subscription for user."""
        result = await self.session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.is_active == True,
                    Subscription.end_date > datetime.utcnow()
                )
            ).order_by(desc(Subscription.end_date))
        )
        return result.scalars().first()
    
    async def get_by_id(self, subscription_id: int) -> Subscription | None:
        """Get subscription by ID."""
        return await self.session.get(Subscription, subscription_id)
    
    async def create(
        self,
        user_id: int,
        subscription_type: SubscriptionType,
        days: int,
        auto_renewal: bool = True
    ) -> Subscription:
        """Create new subscription."""
        now = datetime.utcnow()
        subscription = Subscription(
            user_id=user_id,
            type=subscription_type,
            start_date=now,
            end_date=now + timedelta(days=days),
            is_active=True,
            auto_renewal=auto_renewal
        )
        self.session.add(subscription)
        await self.session.flush()
        logger.info(f"Created {subscription_type} subscription for user {user_id}")
        return subscription
    
    async def deactivate(self, subscription_id: int) -> None:
        """Deactivate subscription."""
        subscription = await self.get_by_id(subscription_id)
        if subscription:
            subscription.is_active = False
            await self.session.flush()
            logger.info(f"Deactivated subscription {subscription_id}")
    
    async def get_expired(self) -> list[Subscription]:
        """Get all expired active subscriptions."""
        result = await self.session.execute(
            select(Subscription).where(
                and_(
                    Subscription.is_active == True,
                    Subscription.end_date <= datetime.utcnow()
                )
            )
        )
        return result.scalars().all()
