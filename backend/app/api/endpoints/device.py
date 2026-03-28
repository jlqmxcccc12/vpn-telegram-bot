from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from app.schemas import DeviceCreate, DeviceResponse
from app.repository.device_repo import DeviceRepository
from app.utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/{user_id}", response_model=DeviceResponse)
async def create_device(
    user_id: int,
    device_create: DeviceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new device for user."""
    repo = DeviceRepository(session)
    
    # Check device limit
    device_count = await repo.count_user_devices(user_id)
    if device_count >= settings.max_devices_per_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {settings.max_devices_per_user} devices per user allowed"
        )
    
    device = await repo.create(user_id=user_id, name=device_create.name)
    await session.commit()
    
    logger.info(f"Created device {device.id} for user {user_id}")
    return device


@router.get("/{user_id}")
async def list_devices(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get all devices for user."""
    repo = DeviceRepository(session)
    devices = await repo.get_user_devices(user_id)
    return devices


@router.delete("/{device_id}")
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete device."""
    repo = DeviceRepository(session)
    device = await repo.get_by_id(device_id)
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    await repo.delete(device_id)
    await session.commit()
    
    logger.info(f"Deleted device {device_id}")
    return {"message": "Device deleted"}
