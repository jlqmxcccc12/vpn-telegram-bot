# VPN SaaS System - WireGuard Telegram Bot

**Production-ready WireGuard VPN sales platform via Telegram with automated subscription management.**

## Features

✅ **Core Features**
- 🤖 Telegram bot for VPN sales via Telegram Stars
- 🛡️ WireGuard VPN with automatic client management
- 💳 Payment processing (Telegram Stars)
- 📱 Multi-device support (3 devices per user)
- ⏰ Subscription management (Trial, Weekly, Monthly)
- 🔐 End-to-end encryption for private keys (Fernet)
- 🔄 Multi-server support with load balancing
- ⚡ Async/await throughout (FastAPI, aiogram 3.x)

**Anti-Abuse & Security**
- Trial protection (1 per user, non-renewable)
- Device limit enforcement
- Encrypted private key storage
- Telegram ID-based verification
- Secret-based API authentication

**Operations**
- Background task scheduler (subscription expiry cleanup)
- Structured JSON logging
- Docker Compose setup
- Nginx reverse proxy
- Database migrations (Alembic)

## Architecture

```
Telegram User
    ↓
Telegram Bot (aiogram 3.x)
    ↓
Backend API (FastAPI)
    ↓
VPN Service Layer
    ↓
WireGuard Servers (Multi)
```

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Redis
- Pydantic
- APScheduler

**Bot:**
- aiogram 3.x
- httpx (async HTTP client)
- qrcode (config generation)
- Pillow

**VPN Manager:**
- FastAPI
- WireGuard CLI
- subprocess management

**Infrastructure:**
- Docker
- Docker Compose
- Nginx
- PostgreSQL 15
- Redis 7

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/jlqmxcccc12/vpn-telegram-bot.git
cd vpn-telegram-bot
```

### 2. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `TELEGRAM_BOT_TOKEN` - Get from @BotFather
- `FERNET_KEY` - Generate: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
- `SECRET_KEY` - Random 32+ char string
- Database credentials

### 3. Generate Fernet Key (if needed)

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### 4. Start Services

```bash
docker-compose up -d
```

Services will start:
- `PostgreSQL` on port 5432
- `Redis` on port 6379
- `Backend API` on port 8000
- `WG Manager` on port 8001
- `Nginx` on ports 80/443
- `Telegram Bot` (no port, uses polling)

### 5. Initialize Database

```bash
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

### 6. Check Health

```bash
curl http://localhost/health
```

## API Endpoints

### Users
- `POST /api/users/` - Create user + assign trial
- `GET /api/users/{user_id}` - Get user info
- `GET /api/users/telegram/{telegram_id}` - Get by Telegram ID

### Devices
- `POST /api/devices/{user_id}` - Create device
- `GET /api/devices/{user_id}` - List user devices
- `DELETE /api/devices/{device_id}` - Delete device

### Subscriptions
- `GET /api/subscriptions/user/{user_id}` - Get active subscription
- `GET /api/subscriptions/{subscription_id}` - Get subscription details

### Webhooks
- `POST /api/webhooks/successful_payment` - Process payment webhook

### Health
- `GET /health` - Health check

## Database Schema

### Users
```sql
id | telegram_id | username | trial_used | created_at | updated_at
```

### Subscriptions
```sql
id | user_id | type | start_date | end_date | is_active | auto_renewal
```

### Devices
```sql
id | user_id | name | created_at | updated_at
```

### VPN Clients
```sql
id | device_id | server_id | public_key | private_key_encrypted | ip_address | is_active
```

### Servers
```sql
id | host | public_key | endpoint | endpoint_port | is_active | max_clients
```

### Payments
```sql
id | user_id | telegram_payment_id | amount | subscription_type | status
```

## Configuration

### Subscription Pricing (Telegram Stars)
- Trial: Free, 7 days (1 per user)
- Weekly: 50 ⭐
- Monthly: 150 ⭐

### Feature Limits
- Max devices per user: 3
- Subscription check interval: 5 minutes
- Notification before expiry: 24 hours

### WireGuard
- Default port: 51820
- Default subnet: 10.0.0.0/24
- DNS: 1.1.1.1, 8.8.8.8

## Logs

All services output structured JSON logs to stdout:

```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "level": "INFO",
  "name": "backend.services.vpn_service",
  "message": "Provisioned VPN client on server 1"
}
```

View logs:

```bash
docker-compose logs -f backend
docker-compose logs -f bot
docker-compose logs -f wg-manager
```

## Production Deployment

### 1. SSL/TLS with Let's Encrypt

```bash
mkdir -p nginx/certs
certbot certonly --standalone -d vpn.example.com
cp /etc/letsencrypt/live/vpn.example.com/fullchain.pem nginx/certs/
cp /etc/letsencrypt/live/vpn.example.com/privkey.pem nginx/certs/
```

Update `nginx/nginx.conf` with SSL configuration.

### 2. Environment Security

- Store `.env` in secure vault (not in git)
- Use strong `SECRET_KEY` and `FERNET_KEY`
- Enable `SENTRY_DSN` for error tracking
- Set `BACKEND_DEBUG=false`

### 3. Database Backups

```bash
docker-compose exec postgres pg_dump -U vpn_user -d vpn_db > backup.sql
```

### 4. Monitoring

Enable Sentry for error tracking:

```bash
SENTRY_DSN=https://...@sentry.io/...
```

## Troubleshooting

### Bot not responding
```bash
docker-compose logs bot
# Check TELEGRAM_BOT_TOKEN
```

### Database connection error
```bash
docker-compose exec postgres psql -U vpn_user -d vpn_db
# Verify DATABASE_URL
```

### WireGuard client creation fails
```bash
docker-compose logs wg-manager
# Ensure NET_ADMIN capability is enabled
```

### Payment webhook not received
```bash
# Check webhook configuration in Telegram bot settings
# Verify backend is accessible from Telegram servers
```

## Development

### Run locally (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Bot
cd bot
pip install -r requirements.txt
python main.py

# WG Manager
cd wg-manager
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Database migrations

```bash
docker-compose exec backend alembic revision --autogenerate -m "Your migration"
docker-compose exec backend alembic upgrade head
```

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Security

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Never commit `.env` file** - Use `.env.example` for template
2. **Rotate encryption keys regularly** - Stored in `FERNET_KEY`
3. **Enable HTTPS** - Required for payment processing
4. **Rate limiting** - Implement on production
5. **IP whitelisting** - For WG Manager API
6. **Database encryption** - Enable at rest encryption
7. **Audit logs** - Monitor all payments and subscriptions

## Support

For issues and questions:
- 🐛 [GitHub Issues](https://github.com/jlqmxcccc12/vpn-telegram-bot/issues)
- 💬 [Discussions](https://github.com/jlqmxcccc12/vpn-telegram-bot/discussions)

---

**Made with ❤️ for privacy-conscious users**
