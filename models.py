from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()


class SupportRequest(Base):
    __tablename__ = 'support_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String(50))
    full_name = Column(String(100))
    status = Column(String(20))
    season = Column(Integer)
    contacts = Column(String(200))
    request_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_base():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)