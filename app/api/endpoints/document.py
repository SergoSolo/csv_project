import os
from typing import Optional, TypeVar

import pandas as pd
from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_column, check_document_exists,
                                check_document_format, check_name_duplicate)
from app.core.config import UPLOAD_DIR
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.document import documents_service
from app.schemas.schemas import DocumentSchemaDB
from app.utils import work_with_data

router = APIRouter()
DocumentInformation = TypeVar("DocumentInformation")


@router.get(
        '/',
        summary="Получить список документов.",
        response_model=list[DocumentSchemaDB],
        dependencies=[Depends(current_superuser)]
)
async def get_documents(
    session: AsyncSession = Depends(get_async_session)
) -> list[DocumentSchemaDB]:
    """
    Можно получить список докуметов с общей информацией.
    Доступно только для зарегистрированных пользователей.
    """
    documents = await documents_service.get_all(session)
    return documents


@router.get(
    '/{document_id}',
    response_model=Page,
    summary="Получить определенный файл.",
    dependencies=[Depends(current_superuser)]
)
async def get_document(
    document_id: int,
    column_first: Optional[str | int] = Query(
        None,
        description="Первый столбец фильтрации"
    ),
    value_first: Optional[str | int] = Query(
        None,
        description="Первое значение фильтрации"
    ),
    column_second: Optional[str | int] = Query(
        None,
        description="Второй столбец фильтрации"
    ),
    value_second: Optional[str | int] = Query(
        None,
        description="Второе значение фильтрации"
    ),
    sort_column: Optional[str | int] = Query(
        None, description="Сортировка по столбцу"
    ),
    session: AsyncSession = Depends(get_async_session)
) -> list[DocumentInformation]:
    """
    Доступно только для зарегистрированных пользователей.
    Для получения информации из документа необходимо ввести:

    - **document_id**: Идентификационный номер документа
    - **column_first**: Название столбца для фильтрации данных (Опционально)
    - **value_first**: Значение столбца для фильтрации данных (Опционально)
    - **sort_column**: Название столбца для сортировки данных (Опционально)
    - **page**: Номер страницы (Опционально)
    - **size**: Количество данных выводимых на странице (Опционально)
    """
    document = await check_document_exists(document_id, session)
    document_path = await documents_service.get_object_path(
        object_id=document.id,
        session=session
    )
    data = pd.read_csv(document_path)
    data = data.fillna(0)
    if column_first and value_first:
        check_column(document, column_first)
        data = work_with_data(data, column_first, value_first)
    if column_second and value_second:
        check_column(document, column_second)
        data = work_with_data(data, column_second, value_second)
    if sort_column:
        check_column(document, sort_column)
        data = data.sort_values(by=sort_column)
    return paginate(data.to_dict(orient='records'))


@router.post(
        "/upload",
        summary="Загрузить документ.",
        response_model=DocumentSchemaDB,
        dependencies=[Depends(current_superuser)]
)
async def upload_documentd(
    document: UploadFile,
    session: AsyncSession = Depends(get_async_session)
) -> DocumentSchemaDB:
    """
    Можно загрузить документ только csv формата.
    Доступно только для зарегистрированных пользователей.
    """
    document_name = check_document_format(document.filename)
    await check_name_duplicate(document_name, session)
    document_path = os.path.join(UPLOAD_DIR, f"{document_name}")
    with open(document_path, "wb") as file:
        file.write(document.file.read())
    data = {
        "name": document_name,
        "columns": pd.read_csv(document_path).columns,
        "size": document.size,
        "path": document_path
    }
    document = await documents_service.create(object_in=data, session=session)
    return document


@router.delete(
        "/delete/{document_id}",
        summary="Удалить документ.",
        response_model=DocumentSchemaDB,
        dependencies=[Depends(current_superuser)]
)
async def delete_document(
    document_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> DocumentSchemaDB:
    """
    Доступно только для зарегистрированных пользователей.
    Для удаления документа необходимо ввести:

    - **document_id**: Идентификационный номер документа
    """
    document_path = await documents_service.get_object_path(
        document_id,
        session
    )
    os.remove(document_path)
    document = await documents_service.get_object(document_id, session)
    await documents_service.delete_object(document, session)
    return document
