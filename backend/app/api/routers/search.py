from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.sermon_service import SermonService
from app.services.assistant.content_service import ContentService
from typing import List, Dict, Any

router = APIRouter(prefix="/search", tags=["Global Search"])

@router.get("/", response_model=List[Dict[str, Any]])
def global_search(q: str, db: Session = Depends(get_db)):
    """
    Unified search across Sermons, Prayers, Devotionals, and Conversations.
    """
    if not q:
        return []
        
    query = q.lower()
    sermon_svc = SermonService(db)
    content_svc = ContentService(db)
    
    results = []
    
    try:
        # Search Sermons
        sermons = sermon_svc.list_sermons(limit=100)
        for s in sermons:
            if query in s.title.lower() or (s.theme and query in s.theme.lower()):
                results.append({"type": "Sermon", "id": str(s.id), "title": s.title})
                
        # Search Prayers
        prayers = content_svc.list_prayers()
        for p in prayers:
            if query in p.title.lower():
                results.append({"type": "Prayer", "id": str(p.id), "title": p.title})
                
        # Search Devotionals
        devotionals = content_svc.list_devotionals()
        for d in devotionals:
            if query in d.title.lower():
                results.append({"type": "Devotional", "id": str(d.id), "title": d.title})
    except Exception:
        pass
        
    return results
