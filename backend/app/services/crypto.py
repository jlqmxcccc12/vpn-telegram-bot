from cryptography.fernet import Fernet
from config import settings
import base64


class CryptoService:
    """Service for encrypting/decrypting sensitive data like private keys."""
    
    def __init__(self):
        if not settings.fernet_key:
            raise ValueError("FERNET_KEY not configured")
        self.cipher = Fernet(settings.fernet_key.encode() if isinstance(settings.fernet_key, str) else settings.fernet_key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data."""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt encrypted data."""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()
    
    @staticmethod
    def generate_key() -> str:
        """Generate new Fernet key for configuration."""
        return Fernet.generate_key().decode()
