from app.database.session import SessionLocal
from app.models.domain import BibleBook, BibleChapter, BibleVerse

db = SessionLocal()
print("Books:", db.query(BibleBook).count())
print("Chapters:", db.query(BibleChapter).count())
print("Verses:", db.query(BibleVerse).count())
db.close()
