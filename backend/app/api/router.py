from fastapi import APIRouter
from app.api.endpoints import user, device, subscription, webhook

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(device.router, prefix="/devices", tags=["devices"])
router.include_router(subscription.router, prefix="/subscriptions", tags=["subscriptions"])
router.include_router(webhook.router, prefix="/webhooks", tags=["webhooks"])
