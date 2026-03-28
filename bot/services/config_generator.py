import qrcode, io
from PIL import Image

class ConfigGenerator:
    @staticmethod
    def generate_config(private_key: str, ip: str, server_public_key: str, endpoint: str, endpoint_port: int = 51820) -> str:
        config = f"""[Interface]
PrivateKey = {private_key}
Address = {ip}/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = {endpoint}:{endpoint_port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
        return config

class QRCodeGenerator:
    @staticmethod
    def generate_qr(config_text: str) -> io.BytesIO:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(config_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io