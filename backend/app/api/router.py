from fastapi import APIRouter
from app.api.routers.system import router as system_router
from app.api.routers.conversation import router as conversation_router
from app.api.routers.assistant import router as assistant_router
from app.api.routers.projects import router as projects_router
from app.api.routers.settings import router as settings_router
from app.api.routers.files import router as files_router
from app.api.routers.search import router as search_router
from app.api.routers import chat
from app.api.routers import bible
from app.api.routers import sermon
from app.api.routers import creative
from app.api.routers import communication

api_router = APIRouter()
api_router.include_router(system_router)
api_router.include_router(conversation_router)
api_router.include_router(assistant_router)
api_router.include_router(projects_router)
api_router.include_router(settings_router)
api_router.include_router(files_router)
api_router.include_router(search_router)
api_router.include_router(chat.router)
api_router.include_router(bible.router)
api_router.include_router(sermon.router)
api_router.include_router(creative.router)
api_router.include_router(communication.router)

