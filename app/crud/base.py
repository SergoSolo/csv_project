from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class CRUDEBase:
    """Базовый класс для работы с моделями."""

    def __init__(self, model) -> None:
        self.model = model

    async def create(
            self,
            object_in: dict,
            session: AsyncSession
    ):
        db_object = self.model(**object_in)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def get_all(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def get_object(
            self,
            object_id: int,
            session: AsyncSession
    ):
        db_object = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return db_object.scalars().first()

    async def delete_object(
        self,
        db_object: ModelType,
        session: AsyncSession
    ):
        await session.delete(db_object)
        await session.commit()
