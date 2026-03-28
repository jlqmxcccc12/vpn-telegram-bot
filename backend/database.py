from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from config import settings
from models import Base

engine = create_async_engine(
    settings.database_url,
    echo=settings.backend_debug,
    poolclass=NullPool,
    connect_args={
        "timeout": 10,
        "command_timeout": 10,
    }
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting async session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
