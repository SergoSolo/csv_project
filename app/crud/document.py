from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDEBase
from app.models import Document


class CRUDEDocument(CRUDEBase):
    """Класс для работы с моделью Document."""

    async def get_document_id_by_name(
            self,
            document_name: str,
            session: AsyncSession
    ):
        db_object = await session.execute(
            select(self.model.id).where(self.model.name == document_name)
        )
        return db_object.scalars().first()

    async def get_object_path(
            self,
            object_id: int,
            session: AsyncSession
    ):
        db_object = await session.execute(
            select(self.model.path).where(self.model.id == object_id)
        )
        return db_object.scalars().first()


documents_service = CRUDEDocument(Document)
