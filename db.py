from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, unique=True, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    subscribed = Column(Boolean, default=False)
    registered = Column(Boolean, default=False)


engine = create_async_engine("sqlite+aiosqlite:///webinar.db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
