from app.database.session import SessionLocal
from app.models.domain import BibleTranslation

db = SessionLocal()
trans = db.query(BibleTranslation).all()
for t in trans:
    print(t.code, t.name)
db.close()
