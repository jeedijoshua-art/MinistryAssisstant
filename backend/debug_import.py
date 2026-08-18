import os
import json
from app.database.session import SessionLocal
from app.models.domain import BibleBook, BibleTranslation, BibleChapter, BibleVerse
from app.services.bible.import_service import BibleImportService

db = SessionLocal()
# Wipe everything
db.query(BibleVerse).delete()
db.query(BibleChapter).delete()
db.query(BibleBook).delete()
db.query(BibleTranslation).delete()
db.commit()

# Create translation
from uuid import uuid4
trans_id = uuid4()
db.add(BibleTranslation(id=trans_id, code="TEST", name="Test Version", language="English"))
db.commit()

print("Translation TEST exists. Books count:", db.query(BibleBook).count())

with open("mock_bible.json", "r") as f:
    content = f.read()

svc = BibleImportService(db)
stats = svc.import_json(content)
print(stats)
