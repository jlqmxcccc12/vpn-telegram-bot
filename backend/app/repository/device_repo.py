from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Device, VPNClient
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DeviceRepository:
    """Repository for device operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, device_id: int) -> Device | None:
        """Get device by ID."""
        return await self.session.get(Device, device_id)
    
    async def get_user_devices(self, user_id: int) -> list[Device]:
        """Get all devices for user."""
        result = await self.session.execute(
            select(Device).where(Device.user_id == user_id)
        )
        return result.scalars().all()
    
    async def count_user_devices(self, user_id: int) -> int:
        """Count user devices."""
        result = await self.session.execute(
            select(func.count(Device.id)).where(Device.user_id == user_id)
        )
        return result.scalar()
    
    async def create(self, user_id: int, name: str) -> Device:
        """Create new device."""
        device = Device(
            user_id=user_id,
            name=name
        )
        self.session.add(device)
        await self.session.flush()
        logger.info(f"Created device {device.id} for user {user_id}")
        return device
    
    async def delete(self, device_id: int) -> None:
        """Delete device."""
        device = await self.get_by_id(device_id)
        if device:
            await self.session.delete(device)
            await self.session.flush()
            logger.info(f"Deleted device {device_id}")
