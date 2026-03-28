# 🚀 ПРАКТИЧЕСКИЙ ГАЙД ПО РАЗВЁРТЫВАНИЮ

## ЧАСТЬ 1: ПОДГОТОВКА (15 минут)

### Шаг 1: Установка Docker & Docker Compose

#### На Windows:
```bash
# 1. Скачать Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. Установить
# Пройти через установщик

# 3. Проверить
docker --version
docker-compose --version
```

#### На macOS:
```bash
brew install docker docker-compose
# Или скачать Docker Desktop
docker --version
docker-compose --version
```

#### На Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker

# Проверить
docker --version
docker-compose --version
```

### Шаг 2: Клонировать репозиторий

```bash
git clone https://github.com/jlqmxcccc12/vpn-telegram-bot.git
cd vpn-telegram-bot
```

### Шаг 3: Подготовить переменные окружения

```bash
cp .env.example .env
```

Открыть `.env` в редакторе и заполнить **ОБЯЗАТЕЛЬНЫЕ** переменные.

---

## ЧАСТЬ 2: ГЕНЕРАЦИЯ КЛЮЧЕЙ (10 минут)

### Ключ 1: Telegram Bot Token

**Где получить:**
1. Telegram → @BotFather
2. Отправить `/newbot`
3. Следовать инструкциям
4. Получить token вида: `123456789:ABCDefGHIJKlmnoPQRstUVWxyz`

**В .env:**
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIJKlmnoPQRstUVWxyz
```

### Ключ 2: Fernet Key (шифрование)

**Генерировать:**
```bash
python3 << 'EOF'
from cryptography.fernet import Fernet
key = Fernet.generate_key().decode()
print(f"FERNET_KEY={key}")
EOF
```

**Вывод:**
```
FERNET_KEY=gAAAAABl5m7K4bJ9...[длинная строка]
```

**В .env:**
```bash
FERNET_KEY=gAAAAABl5m7K4bJ9...[вставить сюда]
```

### Ключ 3: Secret Key (API безопасность)

**Генерировать:**
```bash
python3 << 'EOF'
import secrets
key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={key}")
EOF
```

**В .env:**
```bash
SECRET_KEY=[вставить сюда]
```

### Ключ 4: WG Manager Secret

**Генерировать:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(16))"
```

**В .env:**
```bash
WG_MANAGER_SECRET=[вставить сюда]
```

---

## ЧАСТЬ 3: ПРОВЕРКА .env (5 минут)

Открыть `.env` и убедиться:

```bash
# ===== DATABASE =====
DATABASE_URL=postgresql+asyncpg://vpn_user:vpn_password@postgres:5432/vpn_db
REDIS_URL=redis://redis:6379/0

# ===== TELEGRAM BOT =====
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIJKlmnoPQRstUVWxyz  # ✅ ТВОЙ TOKEN

# ===== BACKEND API =====
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_DEBUG=false  # true только в разработке
SECRET_KEY=...  # ✅ ТВОЙ КЛЮЧ

# ===== ENCRYPTION =====
FERNET_KEY=...  # ✅ ТВОЙ КЛЮЧ

# ===== WG MANAGER =====
WG_MANAGER_HOST=wg-manager
WG_MANAGER_PORT=8001
WG_MANAGER_SECRET=...  # ✅ ТВОЙ КЛЮЧ

# ===== POSTGRES =====
POSTGRES_USER=vpn_user  # Менять не обязательно
POSTGRES_PASSWORD=vpn_password  # Менять не обязательно
POSTGRES_DB=vpn_db
```

---

## ЧАСТЬ 4: ПЕРВЫЙ ЗАПУСК (20 минут)

### Шаг 1: Собрать образы

```bash
docker-compose build
```

**Это займёт 3-5 минут.** Терпеливо ждите.

**Вывод будет примерно такой:**
```
Building postgres ... done
Building redis ... done
Building backend ... done
Building bot ... done
Building wg-manager ... done
Building nginx ... done
```

### Шаг 2: Запустить сервисы

```bash
docker-compose up -d
```

**Проверить что запустилось:**
```bash
docker-compose ps
```

**Должно быть:**
```
NAME                  COMMAND                  STATE      PORTS
postgres              postgres                 Up         5432/tcp
redis                 redis-server             Up         6379/tcp
backend               uvicorn main:app         Up         8000/tcp
bot                   python main.py           Up
wg-manager            uvicorn main:app         Up         8001/tcp
nginx                 nginx -g daemon off      Up         80/tcp, 443/tcp
```

### Шаг 3: Ждать полной инициализации (30 сек)

```bash
sleep 30
```

### Шаг 4: Инициализировать БД

```bash
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

**Вывод:**
```
Tables created successfully
```

### Шаг 5: Проверить здоровье сервисов

```bash
curl http://localhost/health
```

**Должно вернуть:**
```json
{"status": "healthy"}
```

---

## ЧАСТЬ 5: ТЕСТИРОВАНИЕ ЛОКАЛЬНО (15 минут)

### Тест 1: Backend API

**Swagger UI:**
```
http://localhost:8000/docs
```

Открыть в браузере. Должна быть интерактивная документация.

**Тест создания пользователя:**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456789, "username": "testuser"}'
```

**Ответ:**
```json
{
  "id": 1,
  "telegram_id": 123456789,
  "username": "testuser",
  "trial_used": false,
  "created_at": "2024-01-01T12:00:00"
}
```

### Тест 2: Telegram Bot

**Открыть Telegram:**
1. Найти своего бота (@BotFather → токен)
2. Нажать /start
3. Должно быть сообщение: "Добро пожаловать! У вас есть 7 дней бесплатного доступа"
4. Появятся кнопки:
   - 🚀 Get VPN
   - 💳 Buy / 👤 Profile
   - 📱 Instructions

**Логи:**
```bash
docker-compose logs -f bot
```

### Тест 3: WireGuard Manager

```bash
curl -H "X-Secret: [твой WG_MANAGER_SECRET]" \
  http://localhost:8001/api/servers/1
```

**Ответ:**
```json
{
  "server_id": 1,
  "status": "active",
  "clients": 0
}
```

### Тест 4: Логи всех сервисов

```bash
# Backend
docker-compose logs -f backend

# Bot
docker-compose logs -f bot

# WG Manager
docker-compose logs -f wg-manager

# База данных
docker-compose logs -f postgres
```

---

## ЧАСТЬ 6: ПОДКЛЮЧЕНИЕ К БД (опционально)

**Если хочешь посмотреть данные в БД:**

### Option 1: Из командной строки

```bash
docker-compose exec postgres psql -U vpn_user -d vpn_db
```

**Команды SQL:**
```sql
-- Посмотреть таблицы
\dt

-- Посмотреть пользователей
SELECT * FROM users;

-- Посмотреть подписки
SELECT * FROM subscriptions;

-- Выход
\q
```

### Option 2: GUI (pgAdmin)

**Добавить в docker-compose.yml:**
```yaml
pgadmin:
  image: dpage/pgadmin4
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  networks:
    - vpn-network
```

**Потом:**
```bash
docker-compose up -d pgadmin
```

**Открыть:** http://localhost:5050
- Email: admin@example.com
- Password: admin

---

## ЧАСТЬ 7: РАЗРАБОТКА & ОТЛАДКА

### Вкл. Debug Mode

**В .env:**
```bash
BACKEND_DEBUG=true
LOG_LEVEL=DEBUG
```

**Перезагрузить:**
```bash
docker-compose restart backend
```

### Просмотр логов в реальном времени

```bash
# Все сразу
docker-compose logs -f

# Только ошибки
docker-compose logs -f | grep ERROR

# Последние 100 строк
docker-compose logs --tail=100
```

### Вход в контейнер

```bash
# Backend
docker-compose exec backend bash

# Bot
docker-compose exec bot bash

# WireGuard
docker-compose exec wg-manager bash
```

### Перезагрузить сервис

```bash
docker-compose restart backend
# или
docker-compose up -d --force-recreate backend
```

---

## ЧАСТЬ 8: ОСТАНОВКА & ОЧИСТКА

### Остановить (сохранить данные)

```bash
docker-compose stop
```

### Запустить снова

```bash
docker-compose start
```

### Полная остановка (удалить контейнеры)

```bash
docker-compose down
```

### Удалить всё включая БД

```bash
docker-compose down -v
```

⚠️ **ВНИМАНИЕ:** Это удалит все данные в базе!

---

## ЧАСТЬ 9: РАЗВЁРТЫВАНИЕ НА VPS (для production)

### Требования к VPS:
- **OS:** Ubuntu 20.04 или новее
- **CPU:** 2 cores
- **RAM:** 4GB
- **Storage:** 50GB SSD
- **Ports:** 80, 443, 22 открыты

### Шаг 1: SSH на сервер

```bash
ssh root@your_vps_ip
```

### Шаг 2: Обновить систему

```bash
sudo apt update && sudo apt upgrade -y
```

### Шаг 3: Установить Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker root
```

### Шаг 4: Установить Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Шаг 5: Клонировать проект

```bash
cd /opt
git clone https://github.com/jlqmxcccc12/vpn-telegram-bot.git
cd vpn-telegram-bot
```

### Шаг 6: Подготовить .env

```bash
cp .env.example .env
nano .env  # или vim
```

**Важные изменения для production:**
```bash
BACKEND_DEBUG=false
BACKEND_HOST=0.0.0.0
DOMAIN=your_domain.com  # Твой домен
```

### Шаг 7: Запустить

```bash
docker-compose up -d
docker-compose logs -f
```

### Шаг 8: Настроить SSL (HTTPS)

**Установить Certbot:**
```bash
sudo apt install certbot -y
```

**Получить сертификат:**
```bash
sudo certbot certonly --standalone -d your_domain.com
```

**Обновить nginx.conf:**
```bash
# Скопировать пути сертификатов в nginx.conf
ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
```

**Перезагрузить Nginx:**
```bash
docker-compose restart nginx
```

### Шаг 9: Автообновление сертификата

```bash
sudo crontab -e
```

**Добавить:**
```
0 0 1 * * certbot renew --quiet && docker-compose restart nginx
```

---

## ЧАСТЬ 10: ЧАСТЫЕ ОШИБКИ И РЕШЕНИЯ

### Ошибка: "Connection refused"

```bash
# Проверить запущены ли контейнеры
docker-compose ps

# Если не запущены
docker-compose up -d

# Проверить логи
docker-compose logs postgres
```

### Ошибка: "Database connection failed"

```bash
# Переинициализировать БД
docker-compose down -v
docker-compose up -d
sleep 30
docker-compose exec backend python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

### Ошибка: "Bot not responding"

```bash
# Проверить токен
echo $TELEGRAM_BOT_TOKEN

# Проверить логи
docker-compose logs -f bot | grep -i token

# Перезагрузить
docker-compose restart bot
```

### Ошибка: "Port already in use"

```bash
# Найти какой процесс занял порт
sudo lsof -i :8000

# Или в .env изменить порты
BACKEND_PORT=8001
```

### Ошибка: "Out of memory"

```bash
# Проверить использование
docker stats

# Очистить неиспользуемые образы
docker system prune -a

# Ограничить память для контейнера в docker-compose.yml
mem_limit: 1gb
```

---

## ЧАСТЬ 11: MONITORING & ЛОГИРОВАНИЕ

### Просмотр логов

```bash
# Все логи в реальном времени
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Последние N строк
docker-compose logs --tail=50 backend

# Сохранить в файл
docker-compose logs backend > backend.log
```

### Использование ресурсов

```bash
# Реальное время
docker stats

# Информация контейнера
docker inspect vpn-telegram-bot_backend_1
```

### Резервная копия БД

```bash
# Сделать dump
docker-compose exec postgres pg_dump -U vpn_user -d vpn_db > backup.sql

# Восстановить
cat backup.sql | docker-compose exec -T postgres psql -U vpn_user -d vpn_db
```

---

## ЧАСТЬ 12: ГОТОВО К PRODUCTION! ✅

**Чеклист:**
- [x] Docker установлен
- [x] Проект клонирован
- [x] .env заполнен
- [x] Сервисы запущены
- [x] API отвечает
- [x] Bot отвечает
- [x] БД инициализирована
- [x] SSL настроен (для VPS)
- [x] Логирование включено
- [x] Резервная копия готова

**Теперь можно:**
✅ Добавлять реальных пользователей
✅ Принимать платежи (Telegram Stars)
✅ Раздавать VPN configs
✅ Масштабировать при необходимости

---

## КОНТАКТЫ & ПОДДЕРЖКА

📝 **Issues & Questions:** GitHub Issues
💬 **Discussions:** GitHub Discussions
📚 **Docs:** README.md, ARCHITECTURE.md

**Good luck! 🚀**
