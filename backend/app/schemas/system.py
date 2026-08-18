from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class VersionResponse(BaseModel):
    name: str
    version: str
    environment: str
