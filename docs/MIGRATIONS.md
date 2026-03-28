# Database Migrations

Alembic is configured for database migrations.

## Create Migration

```bash
docker-compose exec backend alembic revision --autogenerate -m "Add user column"
```

## Apply Migrations

```bash
docker-compose exec backend alembic upgrade head
```

## Rollback

```bash
docker-compose exec backend alembic downgrade -1
```

## View History

```bash
docker-compose exec backend alembic history
```

## Current Version

```bash
docker-compose exec backend alembic current
```

## Database Schema

See README.md for detailed schema information.
