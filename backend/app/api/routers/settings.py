from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.domain import ChurchProfile
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/settings", tags=["Settings"])

class ChurchProfileSchema(BaseModel):
    church_name: str
    pastor_name: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None

@router.get("/profile", response_model=ChurchProfileSchema)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(ChurchProfile).first()
    if not profile:
        profile = ChurchProfile(church_name="Grace Community Church")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.post("/profile", response_model=ChurchProfileSchema)
def update_profile(data: ChurchProfileSchema, db: Session = Depends(get_db)):
    profile = db.query(ChurchProfile).first()
    if not profile:
        profile = ChurchProfile(**data.dict())
        db.add(profile)
    else:
        for k, v in data.dict().items():
            setattr(profile, k, v)
    db.commit()
    db.refresh(profile)
    return profile
