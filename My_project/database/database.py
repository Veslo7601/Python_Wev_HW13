from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres_async"

async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def async_get_database() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
