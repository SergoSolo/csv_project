import os
from http import HTTPStatus

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.core.db import AsyncSession
from app.crud.document import documents_service
from app.models import Document


async def check_document_exists(
        document_id: int,
        session: AsyncSession,
) -> Document:
    """Проверка наличия документа в db."""
    document = await documents_service.get_object(document_id, session)
    if document is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Документ не найден!"
        )
    return document


async def check_name_duplicate(
        document_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени."""
    document_id = await documents_service.get_document_id_by_name(
        document_name,
        session
    )
    if document_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Документ с таким именем уже существует!",
        )


def check_document_format(
        document_name: str
) -> str:
    """Проверка формата документа."""
    document_format = os.path.splitext(document_name)[1]
    if document_format != '.csv':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Поддерживается только документы csv формата!",
        )
    return document_name


def check_column(document: Document, column: str) -> None:
    """
    Проверка введенных пользователем столбцов,
    для фильтрации или сортировки.
    """
    if column not in document.columns:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f"В файле нет столбца {column}. "
                "Проверьте правильно ли ввели название."
            ),
        )


def check_document_is_empty(document: UploadFile) -> pd.DataFrame:
    """Проверка пуст ли документ."""
    try:
        document = pd.read_csv(document)
        return document
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Документ пуст!",
        )
