from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import User
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class UserRepository:
    """Repository for user operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
    
    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        return await self.session.get(User, user_id)
    
    async def create(self, telegram_id: int, username: str | None = None) -> User:
        """Create new user."""
        user = User(
            telegram_id=telegram_id,
            username=username,
            trial_used=False
        )
        self.session.add(user)
        await self.session.flush()
        logger.info(f"Created user {user.id} with telegram_id {telegram_id}")
        return user
    
    async def update_trial_used(self, user_id: int) -> None:
        """Mark trial as used."""
        user = await self.get_by_id(user_id)
        if user:
            user.trial_used = True
            await self.session.flush()
            logger.info(f"Marked trial as used for user {user_id}")
    
    async def count(self) -> int:
        """Get total user count."""
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar()
