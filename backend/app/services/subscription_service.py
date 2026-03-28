from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from models import SubscriptionType, User
from app.repository.user_repo import UserRepository
from app.repository.subscription_repo import SubscriptionRepository
from app.utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)


class SubscriptionService:
    """Service for subscription management."""
    
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session
        self.user_repo = UserRepository(session)
        self.sub_repo = SubscriptionRepository(session)
    
    async def get_or_create_subscription(
        self,
        user: User,
        subscription_type: SubscriptionType
    ) -> bool:
        """Get active subscription or create new one if needed.
        
        Returns True if subscription was created/activated, False if already active.
        """
        # Check for active subscription
        active = await self.sub_repo.get_active_by_user(user.id)
        if active:
            # Already has active subscription
            return False
        
        # Get subscription duration
        days = self._get_subscription_days(subscription_type)
        
        # Create new subscription
        await self.sub_repo.create(
            user_id=user.id,
            subscription_type=subscription_type,
            days=days,
            auto_renewal=True
        )
        
        return True
    
    async def get_trial_subscription(self, user: User) -> bool:
        """Try to give trial subscription.
        
        Returns True if trial was activated, False if already used.
        """
        if user.trial_used:
            return False
        
        # Create trial subscription
        await self.sub_repo.create(
            user_id=user.id,
            subscription_type=SubscriptionType.TRIAL,
            days=settings.trial_days,
            auto_renewal=False
        )
        
        # Mark trial as used
        await self.user_repo.update_trial_used(user.id)
        logger.info(f"Activated trial for user {user.id}")
        
        return True
    
    async def deactivate_expired_subscriptions(self) -> int:
        """Deactivate all expired subscriptions.
        
        Returns count of deactivated subscriptions.
        """
        expired = await self.sub_repo.get_expired()
        
        for subscription in expired:
            await self.sub_repo.deactivate(subscription.id)
        
        logger.info(f"Deactivated {len(expired)} expired subscriptions")
        return len(expired)
    
    @staticmethod
    def _get_subscription_days(subscription_type: SubscriptionType) -> int:
        """Get subscription duration in days."""
        if subscription_type == SubscriptionType.TRIAL:
            return settings.trial_days
        elif subscription_type == SubscriptionType.WEEKLY:
            return 7
        elif subscription_type == SubscriptionType.MONTHLY:
            return 30
        else:
            return 30
    
    @staticmethod
    def get_subscription_price(subscription_type: SubscriptionType) -> int:
        """Get subscription price in Telegram Stars."""
        if subscription_type == SubscriptionType.TRIAL:
            return 0
        elif subscription_type == SubscriptionType.WEEKLY:
            return settings.weekly_price
        elif subscription_type == SubscriptionType.MONTHLY:
            return settings.monthly_price
        else:
            return 0
