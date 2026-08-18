import argparse
import sys
import logging
from app.database.session import SessionLocal
from app.services.bible.import_service import BibleImportService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Import a JSON Bible into the database.")
    parser.add_argument("filepath", type=str, help="Path to the JSON file.")
    args = parser.parse_args()

    try:
        with open(args.filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {args.filepath}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        sys.exit(1)

    db = SessionLocal()
    try:
        service = BibleImportService(db)
        stats = service.import_json(content)
        logger.info(f"Successfully imported translation {stats['translation']}.")
        logger.info(f"Books: {stats['books_imported']}")
        logger.info(f"Chapters: {stats['chapters_imported']}")
        logger.info(f"Verses: {stats['verses_imported']}")
    except ValueError as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
