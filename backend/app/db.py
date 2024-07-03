from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

import settings

LocalSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_async_engine(settings.db_async_uri),
)


async def get_db_session():
    session = LocalSession()
    try:
        yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
