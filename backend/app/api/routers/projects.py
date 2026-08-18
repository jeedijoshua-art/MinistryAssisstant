from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.sermon_service import SermonService
from app.services.assistant.content_service import ContentService
from typing import List, Dict, Any

router = APIRouter(prefix="/projects", tags=["Projects Workspace"])

@router.get("/", response_model=List[Dict[str, Any]])
def list_projects(db: Session = Depends(get_db)):
    """
    Returns a unified list of all generated projects (Sermons, Prayers, Devotionals, Posters).
    """
    sermon_svc = SermonService(db)
    content_svc = ContentService(db)
    
    projects = []
    
    # Fetch Sermons
    try:
        sermons = sermon_svc.list_sermons(limit=50)
        for s in sermons:
            projects.append({
                "id": str(s.id),
                "title": s.title,
                "type": "Sermon",
                "date": s.updated_at.isoformat() if s.updated_at else s.created_at.isoformat(),
            })
    except Exception:
        pass
        
    # Fetch content (Prayers, Devotionals, etc)
    try:
        prayers = content_svc.list_prayers()
        for p in prayers:
            projects.append({
                "id": str(p.id),
                "title": p.title,
                "type": "Prayer",
                "date": p.updated_at.isoformat() if p.updated_at else p.created_at.isoformat(),
            })
            
        devotionals = content_svc.list_devotionals()
        for d in devotionals:
            projects.append({
                "id": str(d.id),
                "title": d.title,
                "type": "Devotional",
                "date": d.updated_at.isoformat() if d.updated_at else d.created_at.isoformat(),
            })
    except Exception:
        pass
        
    # Sort by date descending
    projects.sort(key=lambda x: x["date"], reverse=True)
    return projects
