import os
from http import HTTPStatus

from fastapi import HTTPException

from app.core.db import AsyncSession
from app.crud.document import documents_service
from app.models import Document


async def check_document_exists(
        document_id: int,
        session: AsyncSession,
) -> Document:
    document = await documents_service.get_object(document_id, session)
    if document is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Документ не найден!'
        )
    return document


async def check_name_duplicate(
        document_name: str,
        session: AsyncSession,
) -> None:
    document_id = await documents_service.get_document_id_by_name(
        document_name,
        session
    )
    if document_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Документ с таким именем уже существует!',
        )


def check_document_format(
        document: str
) -> str:
    document_format = os.path.splitext(document)[1]
    if document_format != '.csv':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Поддерживается только документы csv формата!',
        )
    return document


def check_column(document: Document, column: str) -> None:
    if column not in document.columns:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f"В файле нет столбца {column}. "
                "Проверьте правильно ли ввели название."
            ),
        )