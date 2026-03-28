import httpx
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BackendClient:
    def __init__(self):
        self.base_url = settings.backend_url
    async def create_user(self, telegram_id: int, username: str = None):
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{self.base_url}/users/", json={"telegram_id": telegram_id, "username": username})
            response.raise_for_status()
            return response.json()
    async def get_user_by_telegram(self, telegram_id: int):
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/users/telegram/{telegram_id}")
            response.raise_for_status()
            return response.json()
    async def create_device(self, user_id: int, device_name: str):
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{self.base_url}/devices/{user_id}", json={"name": device_name})
            response.raise_for_status()
            return response.json()
    async def get_active_subscription(self, user_id: int):
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/subscriptions/user/{user_id}")
                response.raise_for_status()
                return response.json()
            except:
                return None
    async def process_payment(self, user_id: int, telegram_payment_id: str, subscription_type: str, amount: int):
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{self.base_url}/webhooks/successful_payment", json={"user_id": user_id, "telegram_payment_id": telegram_payment_id, "subscription_type": subscription_type, "amount": amount})
            response.raise_for_status()
            return response.json()