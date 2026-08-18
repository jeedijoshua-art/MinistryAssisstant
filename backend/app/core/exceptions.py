from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import logging

async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"})

class ZTPAssistantException(Exception):
    """Base exception for ZTP Assistant backend"""
    pass

class ProjectNotFound(ZTPAssistantException):
    pass

class SermonNotFound(ZTPAssistantException):
    pass

class GeminiGenerationFailed(ZTPAssistantException):
    pass

class CloudinaryUploadFailed(ZTPAssistantException):
    pass

class CreativeAssetSaveFailed(ZTPAssistantException):
    pass
