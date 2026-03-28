# 🚀 QUICK START - БЫСТРЫЕ КОМАНДЫ

## Если у тебя уже Ubuntu/Linux с Docker:

### 1️⃣ Первый запуск (скопируй целиком)
```bash
# Перейди в рабочую папку
cd ~
rm -rf vpn-telegram-bot
git clone https://github.com/jlqmxcccc12/vpn-telegram-bot.git
cd vpn-telegram-bot

# Скопируй конфиг
cp .env.example .env

# Генерируй ключи
echo "FERNET_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))' )" >> .env

# Отредактируй .env с Telegram bot token
nano .env  # или vim .env

# Запусти всё
docker-compose build
docker-compose up -d

# Инициализируй БД
sleep 30
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

# Проверь здоровье
curl http://localhost/health
```

### 2️⃣ Проверь что работает
```bash
# Статус всех контейнеров
docker-compose ps

# API Swagger
# http://localhost:8000/docs

# Логи в реальном времени
docker-compose logs -f
```

### 3️⃣ Тестирование через Telegram
1. Открой Telegram
2. Найди своего бота (@BotFather → твой token)
3. Напиши `/start`
4. Должно написать: "🤖 Добро пожаловать! У вас есть 7 дней бесплатного доступа"

---

## Если что-то не работает:

### ❌ Bot не отвечает
```bash
# Проверь логи
docker-compose logs -f bot

# Убедись что TELEGRAM_BOT_TOKEN правильный в .env
cat .env | grep TELEGRAM_BOT_TOKEN

# Перезагрузи бота
docker-compose restart bot
```

### ❌ Backend не запускается
```bash
# Посмотри ошибку
docker-compose logs backend

# Если проблема с БД
docker-compose down -v
docker-compose up -d
sleep 30
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

### ❌ Port занят
```bash
# Найди что занимает порт 8000
sudo lsof -i :8000

# Или измени в .env
BACKEND_PORT=8001
```

### ❌ Нету интернета на сервере
```bash
# Проверь подключение
ping google.com

# Если нет - обнови сетевые параметры
sudo systemctl restart networking
```

---

## Каждый день:

### Запуск
```bash
cd ~/vpn-telegram-bot
docker-compose up -d
```

### Проверка
```bash
docker-compose ps
curl http://localhost/health
```

### Остановка
```bash
docker-compose stop
# или если нужно удалить контейнеры
docker-compose down
```

---

## Полезные команды:

### 🔍 Логи
```bash
# Все логи
docker-compose logs -f

# Только ошибки
docker-compose logs -f | grep ERROR

# Последние 100 строк
docker-compose logs --tail=100

# Сохранить в файл
docker-compose logs > all-logs.txt
```

### 💾 База данных
```bash
# Подключиться к БД
docker-compose exec postgres psql -U vpn_user -d vpn_db

# Посмотреть пользователей
SELECT * FROM users;

# Выход
\q

# Сделать резервную копию
docker-compose exec postgres pg_dump -U vpn_user -d vpn_db > backup.sql

# Восстановить из бэкапа
cat backup.sql | docker-compose exec -T postgres psql -U vpn_user -d vpn_db
```

### 🐳 Docker
```bash
# Статус контейнеров
docker-compose ps

# Использование памяти/CPU
docker stats

# Вход в контейнер
docker-compose exec backend bash

# Перезагрузить сервис
docker-compose restart backend

# Пересоздать контейнер
docker-compose up -d --force-recreate backend

# Удалить всё включая БД
docker-compose down -v
```

### 🧪 Тестирование API
```bash
# Создать пользователя
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456789, "username": "testuser"}'

# Получить пользователя
curl http://localhost:8000/api/users/1

# Создать устройство
curl -X POST http://localhost:8000/api/devices/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "My Device"}'

# Проверить здоровье
curl http://localhost/health
```

---

## На VPS (Production):

### Подключение
```bash
ssh root@your.vps.ip
```

### Установка Docker (если не установлен)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Развёртывание
```bash
cd /opt
git clone https://github.com/jlqmxcccc12/vpn-telegram-bot.git
cd vpn-telegram-bot
cp .env.example .env

# Отредактируй .env
nano .env

# Запусти
docker-compose up -d
sleep 30
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

### SSL (HTTPS)
```bash
# Установи certbot
sudo apt install certbot -y

# Получи сертификат
sudo certbot certonly --standalone -d your-domain.com

# Обновляй автоматически
sudo crontab -e
# Добавь строку:
# 0 0 1 * * certbot renew --quiet && docker-compose restart nginx
```

---

## Если всё сломалось 🔨

```bash
# Полная очистка
docker-compose down -v
rm -rf volumes
rm .env

# Начни заново
cp .env.example .env
# ... заполни .env
docker-compose up -d
sleep 30
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

---

## Где найти помощь?

- 📖 **Документация**: README.md, ARCHITECTURE.md
- 🐛 **Issues**: GitHub Issues
- 💬 **Дискуссии**: GitHub Discussions
- 📺 **Логи**: `docker-compose logs -f`
- 🌐 **API Docs**: http://localhost:8000/docs

---

**Успехов в развёртывании! 🚀**
