#!/bin/bash

# VPN SaaS Setup Script

set -e

echo "====== VPN SaaS Setup ======"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

echo "✅ Docker found"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker Compose found"
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Edit .env with your settings (TELEGRAM_BOT_TOKEN, FERNET_KEY, etc.)"
    echo ""
fi

# Build and start services
echo "🚀 Starting services..."
docker-compose up -d --build

echo "⏳ Waiting for services to be ready..."
sleep 10

# Initialize database
echo "💾 Initializing database..."
docker-compose exec -T backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Services running:"
echo "  📱 Bot: Listening for Telegram messages"
echo "  🌐 Backend API: http://localhost:8000/docs"
echo "  🔧 WG Manager: http://localhost:8001/health"
echo "  💾 PostgreSQL: localhost:5432"
echo "  ⚡ Redis: localhost:6379"
echo "  🔌 Nginx: http://localhost"
echo ""
echo "Logs:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f bot"
echo "  docker-compose logs -f wg-manager"
echo ""
echo "Stop:"
echo "  docker-compose down"
echo ""
