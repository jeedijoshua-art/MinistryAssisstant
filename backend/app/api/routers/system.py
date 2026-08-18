from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import get_db
from app.schemas.system import HealthResponse, VersionResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", service="ztp-assistant-api")


@router.get("/health/database", response_model=HealthResponse)
def database_health_check(db: Session = Depends(get_db)) -> HealthResponse:
    db.execute(text("SELECT 1"))
    return HealthResponse(status="healthy", service="postgresql")


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(name=settings.app_name, version=settings.app_version, environment=settings.app_env)
