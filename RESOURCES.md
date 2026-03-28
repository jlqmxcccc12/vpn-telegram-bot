# 📹 РЕСУРСЫ & ОБУчеНиЕ

## Документация ПРОЕКТА

| Файл | Описание |
|---|---|
| **README.md** | Основная документация, фичи, тех стек |
| **ARCHITECTURE.md** | Комплексная архитектура, дизайн системы |
| **PRACTICAL_DEPLOYMENT.md** | Практическое руководство по развёртыванию |
| **QUICK_START.md** | Быстрые команды для запуска |
| **docs/CLIENT_SETUP.md** | Как пользователю установить WireGuard |
| **docs/WG_MANAGER_API.md** | API документация WG Manager |
| **docs/MIGRATIONS.md** | Миграции базы данных |

---

## Обучающие Материалы

### FastAPI
- 🌐 **Official Docs**: https://fastapi.tiangolo.com/
- 📰 **Tutorial**: https://fastapi.tiangolo.com/tutorial/
- 📚 **Example**: https://github.com/tiangolo/fastapi/tree/master/examples

### SQLAlchemy (Async)
- 🌐 **Async SQLAlchemy**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- 💳 **ORM Tutorial**: https://docs.sqlalchemy.org/en/20/orm/quickstart.html

### aiogram (Telegram Bot)
- 🌐 **Official Docs**: https://docs.aiogram.dev/
- 📰 **Examples**: https://github.com/aiogram/aiogram/tree/dev-3.x/examples
- 💫 **Telegram Bot API**: https://core.telegram.org/bots/api

### Docker
- 🌐 **Official Docs**: https://docs.docker.com/
- 📚 **Docker Compose**: https://docs.docker.com/compose/
- 📰 **Best Practices**: https://docs.docker.com/develop/dev-best-practices/

### PostgreSQL
- 🌐 **Official Docs**: https://www.postgresql.org/docs/
- 💳 **SQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html

### WireGuard
- 🌐 **Official Site**: https://www.wireguard.com/
- 📚 **Installation**: https://www.wireguard.com/install/
- 📰 **Man Pages**: https://man.archlinux.org/man/wg.8

### Redis
- 🌐 **Official Docs**: https://redis.io/documentation
- 📰 **Commands**: https://redis.io/commands/

### Nginx
- 🌐 **Official Docs**: https://nginx.org/en/docs/
- 📚 **Beginner's Guide**: https://nginx.org/en/docs/beginners_guide.html

### Cryptography (Fernet)
- 🌐 **Official Docs**: https://cryptography.io/en/latest/
- 📚 **Fernet**: https://cryptography.io/en/latest/fernet/

---

## Telegram Bot ❤️

### Получение Token
1. Открыть Telegram
2. Написать @BotFather
3. Написать `/newbot`
4. Следовать инструкциям
5. Получить токен

### Истестные Telegram API
- **Bot API**: https://core.telegram.org/bots/api
- **Telegram Stars**: https://core.telegram.org/bots/payments/stars
- **File Upload**: https://core.telegram.org/bots/api#sendphoto

### Тестирование апи Bot

```bash
# Проверить токен
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe

# Гет меню команд
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMyCommands

# Отправить нормативную тестовую сообщение
curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage \
  -d chat_id=<YOUR_USER_ID> \
  -d text="Test message"
```

---

## Полезные инструменты

### Вражески для работы с API
- **Postman**: https://www.postman.com/ - GUI для тестирования API
- **Insomnia**: https://insomnia.rest/ - альтернатива Postman
- **Thunder Client**: VS Code Extension

### База данных
- **pgAdmin**: https://www.pgadmin.org/ - GUI для PostgreSQL
- **DBeaver**: https://dbeaver.io/ - универсальный SQL client

### Отладка
- **VS Code**: https://code.visualstudio.com/ + Docker extension
- **PyCharm**: https://www.jetbrains.com/pycharm/ - профессиональные тоолы

### Monitoring
- **Sentry**: https://sentry.io/ - Error tracking
- **NewRelic**: https://newrelic.com/ - реал-тайм мониторинг
- **Datadog**: https://www.datadoghq.com/ - интегрированные логи

### Deployment
- **Heroku**: https://www.heroku.com/ - простое развертывание
- **DigitalOcean**: https://www.digitalocean.com/ - VPS
- **AWS**: https://aws.amazon.com/ - энтерпрайз
- **Linode**: https://www.linode.com/ - бюджетные VPS
- **GitHub Actions**: https://github.com/features/actions - CI/CD

---

## Лучшие Практики

### Python Code Quality
```bash
# Линтир
 pip install pylint flake8 black

# Форматтер
black backend/
black bot/

# Проверка
flake8 backend/ --max-line-length=120
```

### Testing
```bash
# Unit tests
pip install pytest pytest-asyncio
pytest tests/

# Покрытие
pip install pytest-cov
pytest --cov=backend tests/
```

### Безопасность
```bash
# Проверка на уязвимости
pip install bandit
bandit -r backend/

# SAST
pip install semgrep
semgrep --config=p/security-audit backend/
```

### Документация
```bash
# Auto-generate docs
pip install mkdocs mkdocs-material
mkdocs new .
mkdocs serve
```

---

## Цветные Telegram API

### Emoji для кнопок
```
🚀 - Launch / Start
💳 - Money / Buy
👤 - Profile
📱 - Instructions
✅ - Success
❌ - Error
⚠️ - Warning
🔍 - Search
💾 - Database
🔧 - WireGuard
⏳ - Loading
🔐 - Security
🧪 - Testing
```

### Положительные Emoji
```
�＠ - @
📄 - Document
📅 - Calendar
📆 - Calendar month
🐛 - Bug
🐍 - Snake
🔓 - Settings
🌐 - Globe
📚 - Library
```

---

## Коммунити
 n
### Открытые Проекты
- **GitHub**: https://github.com/ - код
- **GitLab**: https://gitlab.com/ - энтерпрайз
- **Gitea**: https://gitea.io/ - самохостируемый Git

### Обсуждения
- **Reddit**: r/Python, r/Telegram, r/FastAPI
- **Stack Overflow**: https://stackoverflow.com/
- **GitHub Discussions**: https://github.com/jlqmxcccc12/vpn-telegram-bot/discussions

### Конференции
- **PyConf**: PyCon, EuroPython, PyBerlin
- **Python Web Summit**: https://www.pythonwebsummit.com/
- **Telegram Dev**: https://t.me/PythonRussian

---

## Цитаты расворатов

> "Код - это пишется один раз, читается тысячу раз." - Николас Дъто

> "Тестовый код важен как основной код." - Роберт Мартин

> "Документация - это обещание самому себе из будущего." - Unknown

---

## Настройка IDE (рекомендую)

### VS Code
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "ms-python.black-formatter",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### Extensions
- Python
- Pylance
- Black Formatter
- Docker
- PostgreSQL
- REST Client
- Thunder Client
- GitLens

---

## Cheat Sheets

### Docker Commands
```bash
# Build
docker build -t myapp:latest .

# Run
docker run -d -p 8000:8000 myapp:latest

# Logs
docker logs -f container_id

# Exec
docker exec -it container_id bash

# Compose
docker-compose up -d
docker-compose down
docker-compose ps
docker-compose logs
```

### Git Commands
```bash
# Clone
git clone repo_url

# Commit
git add .
git commit -m "message"

# Push
git push origin main

# Pull
git pull origin main

# Branch
git branch feature
git checkout feature
git merge feature
```

### PostgreSQL
```sql
-- Connect
psql -U user -d database

-- List databases
\l

-- List tables
\dt

-- Show table structure
\d table_name

-- Query
SELECT * FROM table_name;

-- Exit
\q
```

### Linux/Bash
```bash
# Navigation
cd directory
ls -la
pwd

# File operations
cat file
echo "text" > file
grep "pattern" file

# Process
ps aux
kill -9 PID

# Network
ping host
netstat -an
ss -ln
```

---

## Прочие Проекты для инспирации

- **Bitwarden**: Password manager - https://github.com/bitwarden/server
- **Home Assistant**: Smart home - https://github.com/home-assistant/core
- **Matrix**: Messenger - https://github.com/matrix-org/synapse
- **Mastodon**: Social Network - https://github.com/mastodon/mastodon
- **Nextcloud**: Cloud Storage - https://github.com/nextcloud/server

---

## Лицензии & Лицензные Настройки

- **MIT**: Простая, популярная
- **Apache 2.0**: Патенты, традемарки
- **GPL 3.0**: Copyleft, открыт источник
- **BSD**: Флексибельная

---

## FAQ (Часто Задаваемые Вопросы)

### Q: Как я могу использовать это в production?
A: См. PRACTICAL_DEPLOYMENT.md, раздел VPS.

### Q: Как добавить свою фичу?
A: Добавь эндпоинт в backend/, гендлер в bot/.

### Q: Как расмасштабировать при большим количестве пользователей?
A: Кубернетес, планируются нагружки.

### Q: А вот мои данные?
A: Encrypted с Fernet, safe. See ARCHITECTURE.md.

---

**Навидитесь на GitHub за пример кода и инструкциями!**

🚀 **Happy Coding!**
