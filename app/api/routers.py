from fastapi import APIRouter

from app.api.endpoints import documents_router, user_router

main_router = APIRouter()

main_router.include_router(
    documents_router,
    prefix="/documents",
    tags=["Работа с документами."]
)
main_router.include_router(user_router)
