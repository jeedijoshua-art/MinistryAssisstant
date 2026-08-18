import sys
import json
import asyncio
from app.database.session import SessionLocal
from app.services.bible.import_service import BibleImportService

def main():
    db = SessionLocal()
    try:
        with open("mock_bible.json", "r") as f:
            content = f.read()
        
        svc = BibleImportService(db)
        stats = svc.import_json(content)
        print("Import successful!")
        print(json.dumps(stats, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
