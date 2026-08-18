from app.database.session import SessionLocal
from app.api.routers.bible import get_bible_service
db = SessionLocal()
svc = get_bible_service(db)
res = svc.resolve_reference("John 3:16", "TEST")
print(res)
