import json
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.models.domain import BibleTranslation, BibleBook, BibleChapter, BibleVerse
from app.services.bible.reference_parser import ReferenceParser

class BibleImportService:
    def __init__(self, db: Session):
        self.db = db

    def import_json(self, file_content: str) -> dict:
        """
        Parses and imports a JSON Bible dataset.
        Returns a dict with import statistics.
        """
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        start_time = time.time()
        logger.info("Loaded JSON")
        
        data = json.loads(file_content)
        
        if isinstance(data, list):
            logger.info("Detected list root")
            code = "KJV"
            name = "King James Version"
            language = "English"
            books = data
        elif isinstance(data, dict):
            logger.info("Detected dict root")
            code = data.get("translation_code")
            name = data.get("translation_name")
            language = data.get("language", "English")
            books = data.get("books", [])
        else:
            raise ValueError("Invalid JSON: Root must be a list or a dictionary.")
            
        if not code or not name:
            raise ValueError("Invalid JSON: Missing translation_code or translation_name")
            
        try:
            # 1. Get or Create Translation
            translation = self.db.query(BibleTranslation).filter(BibleTranslation.code == code).first()
            if not translation:
                translation_id = uuid4()
                translation = BibleTranslation(
                    id=translation_id,
                    code=code,
                    name=name,
                    language=language
                )
                self.db.add(translation)
                self.db.flush()
                logger.info(f"Created new translation: {code}")
            else:
                translation_id = translation.id
                logger.info(f"Reusing existing translation: {code}")
            
            # Fetch existing books, chapters, and verses to prevent duplicates
            existing_books = {b.name.lower(): b.id for b in self.db.query(BibleBook).filter_by(translation_id=translation_id).all()}
            
            books_data = []
            chapters_data = []
            verses_data = []
            
            book_count = 0
            chapter_count = 0
            verse_count = 0
            skipped_duplicates = 0
            
            for book_json in books:
                book_name = book_json.get("name") or book_json.get("book")
                if not book_name:
                    continue
                
                # Normalize book name using ReferenceParser aliases if possible
                normalized_name = ReferenceParser.BOOK_ALIASES.get(book_name.lower(), book_name)
                
                logger.info(f"Importing {normalized_name}")
                
                if normalized_name.lower() in existing_books:
                    book_id = existing_books[normalized_name.lower()]
                    skipped_duplicates += 1
                else:
                    book_id = uuid4()
                    books_data.append({
                        "id": book_id,
                        "translation_id": translation_id,
                        "name": normalized_name,
                        "abbreviation": book_json.get("abbreviation", normalized_name[:3]),
                        "testament": book_json.get("testament", "Unknown"),
                        "book_number": book_json.get("book_number", book_count + len(existing_books) + 1)
                    })
                    existing_books[normalized_name.lower()] = book_id
                    book_count += 1
                
                existing_chapters = {c.chapter_number: c.id for c in self.db.query(BibleChapter).filter_by(book_id=book_id).all()}
                
                for chapter_json in book_json.get("chapters", []):
                    try:
                        chapter_number = int(chapter_json.get("chapter_number") or chapter_json.get("chapter"))
                    except (ValueError, TypeError):
                        continue
                    
                    if chapter_number in existing_chapters:
                        chapter_id = existing_chapters[chapter_number]
                        skipped_duplicates += 1
                    else:
                        chapter_id = uuid4()
                        chapters_data.append({
                            "id": chapter_id,
                            "book_id": book_id,
                            "chapter_number": chapter_number
                        })
                        existing_chapters[chapter_number] = chapter_id
                        chapter_count += 1
                        logger.info(f"Chapter {chapter_number}")
                    
                    existing_verses = {v.verse_number: v.id for v in self.db.query(BibleVerse).filter_by(chapter_id=chapter_id).all()}
                    
                    chapter_verse_count = 0
                    for verse_json in chapter_json.get("verses", []):
                        try:
                            verse_number = int(verse_json.get("verse_number") or verse_json.get("verse"))
                        except (ValueError, TypeError):
                            continue
                        
                        text = verse_json.get("text")
                        if not text:
                            continue
                            
                        if verse_number in existing_verses:
                            skipped_duplicates += 1
                            continue
                            
                        verse_id = uuid4()
                        verses_data.append({
                            "id": verse_id,
                            "chapter_id": chapter_id,
                            "verse_number": verse_number,
                            "text": text
                        })
                        existing_verses[verse_number] = verse_id
                        verse_count += 1
                        chapter_verse_count += 1
                    
                    if chapter_verse_count > 0:
                        logger.info(f"Imported {chapter_verse_count} verses for Chapter {chapter_number}")

            # Execute bulk inserts efficiently
            if books_data:
                self.db.execute(insert(BibleBook), books_data)
            if chapters_data:
                self.db.execute(insert(BibleChapter), chapters_data)
                
            BATCH_SIZE = 5000
            for i in range(0, len(verses_data), BATCH_SIZE):
                batch = verses_data[i:i + BATCH_SIZE]
                self.db.execute(insert(BibleVerse), batch)
                
            self.db.commit()
            
            elapsed = time.time() - start_time
            logger.info("Finished")
            logger.info(f"Books imported: {book_count}")
            logger.info(f"Chapters imported: {chapter_count}")
            logger.info(f"Verses imported: {verse_count}")
            logger.info(f"Skipped duplicates: {skipped_duplicates}")
            logger.info(f"Elapsed time: {elapsed:.2f}s")
            
            return {
                "translation": code,
                "books_imported": book_count,
                "chapters_imported": chapter_count,
                "verses_imported": verse_count,
                "skipped_duplicates": skipped_duplicates,
                "elapsed_seconds": elapsed
            }
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to import Bible JSON: {e}")
