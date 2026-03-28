from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from app.services.subscription_service import SubscriptionService
from app.utils.logger import setup_logger
from config import settings
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = setup_logger(__name__)


def setup_background_tasks(app):
    """Setup background tasks for the application."""
    scheduler = AsyncIOScheduler()
    
    async def cleanup_expired_subscriptions():
        """Cleanup expired subscriptions task."""
        async with AsyncSessionLocal() as session:
            service = SubscriptionService(session)
            count = await service.deactivate_expired_subscriptions()
            logger.info(f"Background task: Deactivated {count} expired subscriptions")
    
    # Add background tasks
    scheduler.add_job(
        cleanup_expired_subscriptions,
        IntervalTrigger(seconds=settings.subscription_check_interval),
        id="cleanup_subscriptions",
        name="Cleanup expired subscriptions",
        replace_existing=True
    )
    
    async def start_scheduler():
        if not scheduler.running:
            scheduler.start()
            logger.info("Background scheduler started")
    
    @app.on_event("startup")
    async def startup():
        await start_scheduler()
    
    @app.on_event("shutdown")
    async def shutdown():
        scheduler.shutdown()
        logger.info("Background scheduler stopped")
