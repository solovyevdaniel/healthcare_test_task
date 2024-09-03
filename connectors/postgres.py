from asyncio import current_task
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PostgresDb:
    def __init__(self, user: str, password: str, host: str, port: str, db_name: str):
        db_url = self._get_url(user, password, host, port, db_name)
        self._engine = create_async_engine(
            db_url,
            future=True,
            pool_recycle=600,
        )
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    def _get_url(self, user: str, password: str, host: str, port: str, db_name: str) -> str:
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

    @property
    def engine(self):
        return self._engine

    @asynccontextmanager
    async def session_factory(
        self, autocommit: bool = True
    ) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            if autocommit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
