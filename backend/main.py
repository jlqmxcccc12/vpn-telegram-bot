from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, init_db
from app.api.router import router
from app.tasks.background import setup_background_tasks
from config import settings
from app.utils.logger import setup_logger
import sentry_sdk

logger = setup_logger(__name__)

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn)

app = FastAPI(
    title="VPN SaaS Backend",
    description="Backend API for WireGuard VPN sales via Telegram",
    version="1.0.0",
    debug=settings.backend_debug
)


@app.on_event("startup")
async def startup():
    """Initialize database and background tasks."""
    logger.info("Starting up...")
    await init_db()
    setup_background_tasks(app)
    logger.info("Startup complete")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    logger.info("Shutting down...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


app.include_router(router, prefix="/api")
