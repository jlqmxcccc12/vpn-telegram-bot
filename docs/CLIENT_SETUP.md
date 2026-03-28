# Client Configuration Template

## File: client.conf

This is an example of what clients receive (automatically generated):

```ini
[Interface]
PrivateKey = <GENERATED_CLIENT_PRIVATE_KEY>
Address = 10.0.0.2/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

## QR Code

Also provided as QR code PNG for easy mobile setup.

## Installation

### Desktop (Linux/Mac/Windows)
1. Download WireGuard from wireguard.com
2. Import the .conf file
3. Connect

### Mobile (Android)
1. Download WireGuard from Play Store
2. Scan QR code with camera
3. Connect

### Mobile (iOS)
1. Download WireGuard from App Store
2. Scan QR code with camera
3. Connect
