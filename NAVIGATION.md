# 🗺️ НАВИГАЦИЯ ПО ПРОЕКТУ (Что читать?)

## 👤 ТЫ НОВИЧОК В ПРОГРАММИРОВАНИИ?

**Начни с этого:**
1. 📖 **BEGINNER_GUIDE.md** - простое объяснение на русском
2. ⚡ **QUICK_START.md** - скопируй команды и запусти
3. 🧪 Протестируй локально
4. 📚 Читай README.md для общего понимания

---

## 🚀 ТЫ ХОЧЕШЬ РАЗВЕРНУТЬ ЭТО БЫСТРО?

**Пошаговая инструкция:**
1. ⚡ **QUICK_START.md** (30 минут)
2. 📝 **PRACTICAL_DEPLOYMENT.md** раздел "Вариант 1: Локально" (15 минут)
3. ✅ Готово!

---

## 🏗️ ТЫ ХОЧЕШЬ ПОНЯТЬ АРХИТЕКТУРУ?

**Для разработчиков:**
1. 📖 **README.md** - обзор
2. 🏛️ **ARCHITECTURE.md** - как всё работает
3. 📚 **Код в backend/** - смотри structure
4. 🔌 **docs/WG_MANAGER_API.md** - интеграция WireGuard

---

## 🌐 ТЫ ХОЧЕШЬ РАЗВЕРНУТЬ НА VPS (Production)?

**Для DevOps:**
1. ⚡ **QUICK_START.md** (если первый раз с Docker)
2. 🚀 **PRACTICAL_DEPLOYMENT.md** раздел "Вариант 2: На VPS"
3. 🔐 Настрой SSL
4. 📊 Раздел "Мониторинг & Логирование"
5. 🔄 Установи auto-renewal сертификатов

---

## 💻 ТЫ ХОЧЕШЬ МОДИФИЦИРОВАТЬ КОД?

**Для разработчиков:**
1. 📖 **ARCHITECTURE.md** - поймешь структуру
2. 📝 **backend/models.py** - начни отсюда (таблицы БД)
3. 📝 **backend/app/services/** - бизнес-логика
4. 📝 **bot/handlers/** - обработчики команд
5. 💡 **docs/WG_MANAGER_API.md** - если меняешь VPN часть
6. 📚 **RESOURCES.md** - полезные ссылки на технологии

---

## 🎓 ТЫ ХОЧЕШЬ ВЫУЧИТЬ ТЕХНОЛОГИИ?

**Обучающие материалы:**
1. 📚 **RESOURCES.md** - все ссылки на документацию
2. 🔗 FastAPI: https://fastapi.tiangolo.com/tutorial/
3. 🔗 SQLAlchemy async: https://docs.sqlalchemy.org/
4. 🔗 aiogram: https://docs.aiogram.dev/
5. 🔗 Docker: https://docs.docker.com/
6. 🔗 PostgreSQL: https://www.postgresql.org/docs/
7. 🔗 WireGuard: https://www.wireguard.com/

---

## 📋 ПОЛНАЯ СТРУКТУРА ДОКУМЕНТАЦИИ

```

├─ 🚀 BEGINNER_GUIDE.md         ← НАЧНИ ОТСЮДА если новичок
├─ ⚡ QUICK_START.md            ← Команды для быстрого запуска
├─ 📖 README.md                 ← Общий обзор проекта
├─ 🏛️ ARCHITECTURE.md           ← Как устроена система
├─ 🔧 PRACTICAL_DEPLOYMENT.md   ← Как развернуть
├─ 📚 RESOURCES.md              ← Ссылки и обучение
├─ 📁 docs/
│  ├─ CLIENT_SETUP.md          ← Как пользователю подключить VPN
│  ├─ WG_MANAGER_API.md        ← API документация WireGuard
│  └─ MIGRATIONS.md            ← Миграции БД
│
├─ 📝 .env.example              ← Шаблон переменных
├─ 🐳 docker-compose.yml        ← Все сервисы в одном файле
├─ 🔧 nginx/nginx.conf          ← Конфиг веб-сервера
│
└─ 💻 backend/, bot/, wg-manager/ ← ТУТ КОД
```

---

## 🎯 СЦЕНАРИИ: "Я ХОЧУ СДЕЛАТЬ..." 

### Сценарий 1: Запустить локально
```bash
👉 Читай: BEGINNER_GUIDE.md → QUICK_START.md
⏱️ Время: 30 минут
```

### Сценарий 2: Развернуть на VPS
```bash
👉 Читай: BEGINNER_GUIDE.md → PRACTICAL_DEPLOYMENT.md (вариант 2)
⏱️ Время: 1-2 часа
```

### Сценарий 3: Модифицировать код
```bash
👉 Читай: ARCHITECTURE.md → Открой IDE → Меняй код
⏱️ Время: Зависит от тебя
```

### Сценарий 4: Добавить новую фичу
```bash
1. Прочитай ARCHITECTURE.md раздел "Структура"
2. Посмотри похожую фичу в коде
3. Скопируй-модифицируй
4. Протестируй локально
5. Разверни
```

### Сценарий 5: Выучить Python/FastAPI
```bash
👉 Читай: RESOURCES.md
👉 Смотри YouTube: "FastAPI tutorial for beginners"
👉 Практикуйся на этом проекте
```

---

## 🆘 ЧТО ДЕЛАТЬ ЕСЛИ...

### ...не запускается локально?
```bash
1. Прочитай BEGINNER_GUIDE.md раздел "Типичные ошибки"
2. Посмотри QUICK_START.md раздел "Ошибки и решения"
3. Включи debug: BACKEND_DEBUG=true в .env
4. Посмотри логи: docker-compose logs -f
5. Откройте Issue на GitHub
```

### ...не получается развернуть на VPS?
```bash
1. Читай PRACTICAL_DEPLOYMENT.md (раздел VPS)
2. Проверь все шаги по порядку
3. Посмотри раздел "Частые ошибки"
4. SSH на сервер и отладь
5. Откройте Issue на GitHub с деталями
```

### ...хочу модифицировать что-то?
```bash
1. Прочитай ARCHITECTURE.md
2. Найди нужный файл в структуре
3. Посмотри похожий код
4. Измени
5. Протестируй: docker-compose restart backend
6. Проверь логи
```

### ...не понимаю как работает часть кода?
```bash
1. Гугли технологию (FastAPI, SQLAlchemy и т.д.)
2. Читай комментарии в коде
3. RESOURCES.md → найди ссылку на документацию
4. Смотри YouTube видео про эту технологию
5. Экспериментируй локально
```

---

## 📊 ПО УРОВНЮ ОПЫТА

### 🟢 Начинающий
1. BEGINNER_GUIDE.md - обязательно
2. QUICK_START.md - скопируй команды
3. Протестируй локально
4. Читай README.md когда захочешь больше знать

### 🟡 Средний
1. ARCHITECTURE.md - поймешь как всё работает
2. PRACTICAL_DEPLOYMENT.md - разверни на VPS
3. Посмотри код в backend/ и bot/
4. RESOURCES.md - выбери технологию для глубокого изучения

### 🔴 Продвинутый
1. ARCHITECTURE.md раздел "Scaling Considerations"
2. Модифицируй код под свои нужды
3. Деплой на Kubernetes
4. Добавь новые фичи
5. Мониторинг (Sentry, etc)

---

## 🎯 ЧИТАЙ В ПОРЯДКЕ ПРИОРИТЕТА

### Если ты спешишь (30 минут)
```
1. BEGINNER_GUIDE.md (5 мин)
2. QUICK_START.md (10 мин)
3. docker-compose up && test (15 мин)
```

### Если у тебя есть час
```
1. BEGINNER_GUIDE.md (10 мин)
2. README.md (15 мин)
3. QUICK_START.md (10 мин)
4. Запусти и протестируй (25 мин)
```

### Если хочешь всё понять (3-4 часа)
```
1. BEGINNER_GUIDE.md (15 мин)
2. README.md (20 мин)
3. ARCHITECTURE.md (30 мин)
4. PRACTICAL_DEPLOYMENT.md (20 мин)
5. Посмотри код (30 мин)
6. Запусти локально (20 мин)
7. Разверни на VPS (1 час)
8. Экспериментируй (оставшееся время)
```

---

## 🔗 БЫСТРЫЕ ССЫЛКИ

### GitHub
- 🔗 **Код**: https://github.com/jlqmxcccc12/vpn-telegram-bot
- 🔗 **Issues**: https://github.com/jlqmxcccc12/vpn-telegram-bot/issues
- 🔗 **Discussions**: https://github.com/jlqmxcccc12/vpn-telegram-bot/discussions

### Технологии
- 🔗 **FastAPI**: https://fastapi.tiangolo.com/
- 🔗 **aiogram**: https://docs.aiogram.dev/
- 🔗 **Docker**: https://docs.docker.com/
- 🔗 **PostgreSQL**: https://www.postgresql.org/docs/

### Телеграм
- 🔗 **BotFather** (создание токена): https://t.me/BotFather
- 🔗 **Bot API docs**: https://core.telegram.org/bots/api
- 🔗 **Telegram Stars**: https://core.telegram.org/bots/payments/stars

---

## 💡 ПО ВОПРОСАМ:

❓ **Как запустить?** → BEGINNER_GUIDE.md + QUICK_START.md
❓ **Как развернуть?** → PRACTICAL_DEPLOYMENT.md  
❓ **Как изменить?** → ARCHITECTURE.md + посмотри код
❓ **Как выучить?** → RESOURCES.md + YouTube
❓ **Что почитать?** → Ты сейчас смотришь этот файл! 👈
❓ **Есть ошибка?** → GitHub Issues

---

## 🎓 ОБРАЗОВАТЕЛЬНЫЙ ПУТЬ

Если хочешь ВЫУЧИТЬСЯ, не просто скопировать-запустить:

```
Шаг 1: Запусти проект локально (BEGINNER_GUIDE.md)
        ↓
Шаг 2: Прочитай как оно работает (ARCHITECTURE.md)
        ↓
Шаг 3: Посмотри код и поймешь каждую строку
        ↓
Шаг 4: Измени что-то маленькое (например, текст приветствия)
        ↓
Шаг 5: Добавь новую фичу (например, новую кнопку)
        ↓
Шаг 6: Разверни на VPS (PRACTICAL_DEPLOYMENT.md)
        ↓
Шаг 7: Используй в production, зарабатывай!
```

---

## ✅ FINAL CHECKLIST

- [ ] Скачал Docker
- [ ] Прочитал BEGINNER_GUIDE.md
- [ ] Запустил QUICK_START.md команды
- [ ] Протестировал локально
- [ ] Прочитал README.md
- [ ] Готов к deployment
- [ ] Понял архитектуру (ARCHITECTURE.md)
- [ ] Готов к модификации кода
- [ ] Готов монетизировать 💰

---

**Успехов в разработке! 🚀**

*Если что-то непонятно - GitHub Issues и Discussions в помощь!*
