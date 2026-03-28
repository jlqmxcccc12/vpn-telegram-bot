# WireGuard Manager API

## Authentication

All requests require `X-Secret` header:

```bash
X-Secret: <WG_MANAGER_SECRET>
```

## Endpoints

### POST /api/clients

Create new VPN client.

**Request:**
```json
{
  "server_id": 1,
  "device_name": "My iPhone"
}
```

**Response:**
```json
{
  "server_id": 1,
  "public_key": "...",
  "private_key": "...",
  "ip": "10.0.0.2",
  "device_name": "My iPhone"
}
```

### DELETE /api/clients/{server_id}

Delete VPN client.

**Request:**
```json
{
  "public_key": "..."
}
```

**Response:**
```json
{
  "message": "Client deleted"
}
```

### GET /api/servers/{server_id}

Get server information.

**Response:**
```json
{
  "server_id": 1,
  "status": "active",
  "clients": 5
}
```

## Key Generation

Keys are generated using WireGuard's `wg` command:

```bash
wg genkey  # Private key
echo <private_key> | wg pubkey  # Public key
```

## IP Assignment

IPs are assigned from the configured subnet (default: 10.0.0.0/24) sequentially.
