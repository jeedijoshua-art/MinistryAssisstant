import os
from app.database.session import SessionLocal
from app.models.domain import BibleBook, BibleTranslation

db = SessionLocal()
# Delete books (cascades or at least we delete them)
db.query(BibleBook).delete()
db.commit()

# Ensure TEST translation exists
trans = db.query(BibleTranslation).filter_by(code="TEST").first()
if not trans:
    from uuid import uuid4
    db.add(BibleTranslation(id=uuid4(), code="TEST", name="Test Version", language="English"))
    db.commit()
db.close()

# Run test_import.py
os.system("PYTHONPATH=. .venv/bin/python test_import.py")
