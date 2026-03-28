import httpx
from config import settings
from app.utils.logger import setup_logger
from typing import Optional

logger = setup_logger(__name__)


class WGManagerClient:
    """HTTP client for WireGuard Manager service."""
    
    def __init__(self):
        self.base_url = f"http://{settings.wg_manager_host}:{settings.wg_manager_port}"
        self.secret = settings.wg_manager_secret
    
    async def create_client(
        self,
        server_id: int,
        device_name: str
    ) -> dict:
        """Create WireGuard client."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.base_url}/api/clients",
                json={
                    "server_id": server_id,
                    "device_name": device_name
                },
                headers={"X-Secret": self.secret}
            )
            response.raise_for_status()
            return response.json()
    
    async def delete_client(self, server_id: int, public_key: str) -> None:
        """Delete WireGuard client."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(
                f"{self.base_url}/api/clients/{server_id}",
                json={"public_key": public_key},
                headers={"X-Secret": self.secret}
            )
            response.raise_for_status()
    
    async def get_server_info(self, server_id: int) -> dict:
        """Get server information."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/servers/{server_id}",
                headers={"X-Secret": self.secret}
            )
            response.raise_for_status()
            return response.json()


class VPNService:
    """Service for VPN operations."""
    
    def __init__(self, wg_client: WGManagerClient):
        self.wg_client = wg_client
    
    async def provision_vpn_client(
        self,
        server_id: int,
        device_name: str
    ) -> dict:
        """Provision new VPN client."""
        try:
            result = await self.wg_client.create_client(server_id, device_name)
            logger.info(f"Provisioned VPN client on server {server_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to provision VPN client: {e}")
            raise
    
    async def remove_vpn_client(
        self,
        server_id: int,
        public_key: str
    ) -> None:
        """Remove VPN client."""
        try:
            await self.wg_client.delete_client(server_id, public_key)
            logger.info(f"Removed VPN client from server {server_id}")
        except Exception as e:
            logger.error(f"Failed to remove VPN client: {e}")
            raise
