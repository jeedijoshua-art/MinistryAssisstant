import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api.router import api_router
from app.config import get_settings
from app.core.exceptions import unhandled_exception_handler
from app.middleware.logging import RequestLoggingMiddleware
from app.core.limiter import limiter

settings = get_settings()
logging.basicConfig(level=logging.DEBUG if settings.app_debug else logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = FastAPI(title=settings.app_name, version=settings.app_version, docs_url="/docs" if settings.app_env != "production" else None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_exception_handler(Exception, unhandled_exception_handler)


from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.session import get_db

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.get("/health/db", tags=["Health"])
def health_db(db: Session = Depends(get_db)):
    try:
        # Check basic connectivity
        db.execute(text("SELECT 1"))
        # Check migrations if alembic_version exists
        version = db.execute(text("SELECT version_num FROM alembic_version")).scalar_one_or_none()
        return {"status": "ok", "database": "connected", "migration_version": version}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(e)})

app.include_router(api_router, prefix=settings.api_v1_prefix)
