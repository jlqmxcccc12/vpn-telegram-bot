import subprocess, re, ipaddress
from utils.logger import setup_logger
from config import settings

logger = setup_logger(__name__)

class WireGuardClient:
    def __init__(self, interface_name: str = "wg0"):
        self.interface_name = interface_name
        self.config_path = f"{settings.wg_config_path}/{interface_name}.conf"
    
    def generate_keypair(self) -> tuple[str, str]:
        private_key = subprocess.check_output(["wg", "genkey"]).decode().strip()
        public_key = subprocess.check_output(["echo", private_key, "|", "wg", "pubkey"], shell=True).decode().strip()
        return private_key, public_key
    
    def add_peer(self, public_key: str, ip: str) -> None:
        try:
            subprocess.run(["wg", "set", self.interface_name, "peer", public_key, "allowed-ips", f"{ip}/32"], check=True)
            logger.info(f"Added peer {public_key} with IP {ip}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error adding peer: {e}")
            raise
    
    def remove_peer(self, public_key: str) -> None:
        try:
            subprocess.run(["wg", "set", self.interface_name, "peer", public_key, "remove"], check=True)
            logger.info(f"Removed peer {public_key}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error removing peer: {e}")
            raise

class IPManager:
    def __init__(self, base_subnet: str = "10.0.0.0/24"):
        self.subnet = ipaddress.ip_network(base_subnet)
        self.used_ips = set()
    
    def assign_ip(self) -> str:
        for ip in self.subnet.hosts():
            if ip not in self.used_ips:
                self.used_ips.add(ip)
                logger.info(f"Assigned IP {ip}")
                return str(ip)
        raise Exception("No available IPs in subnet")
    
    def release_ip(self, ip: str) -> None:
        self.used_ips.discard(ipaddress.ip_address(ip))
        logger.info(f"Released IP {ip}")