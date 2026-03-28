from fastapi import APIRouter, Depends, HTTPException, Header
from services.wg_client import WireGuardClient, IPManager
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api")

wg_client = WireGuardClient()
ip_manager = IPManager()

def verify_secret(x_secret: str = Header(...)) -> str:
    if x_secret != settings.wg_manager_secret:
        raise HTTPException(status_code=401, detail="Invalid secret")
    return x_secret

@router.post("/clients")
async def create_client(server_id: int, device_name: str, _: str = Depends(verify_secret)):
    try:
        private_key, public_key = wg_client.generate_keypair()
        ip = ip_manager.assign_ip()
        wg_client.add_peer(public_key, ip)
        
        return {
            "server_id": server_id,
            "public_key": public_key,
            "private_key": private_key,
            "ip": ip,
            "device_name": device_name
        }
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clients/{server_id}")
async def delete_client(server_id: int, public_key: str, _: str = Depends(verify_secret)):
    try:
        wg_client.remove_peer(public_key)
        return {"message": "Client deleted"}
    except Exception as e:
        logger.error(f"Error deleting client: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/servers/{server_id}")
async def get_server_info(server_id: int, _: str = Depends(verify_secret)):
    return {"server_id": server_id, "status": "active", "clients": len(ip_manager.used_ips)}