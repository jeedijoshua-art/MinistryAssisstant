import re
from typing import Optional, List, Tuple
from pydantic import BaseModel

class ParsedReference(BaseModel):
    book: str
    chapter: Optional[int] = None
    start_verse: Optional[int] = None
    end_verse: Optional[int] = None

class ReferenceParser:
    """Parses natural language Bible references into structured queries."""
    
    # Matches: [Number] [Book Name] [Chapter]:[Verse]-[EndVerse]
    # Examples: John 3:16, 1 Cor 13, 1 John 1:1-4, Ps 23
    PATTERN = re.compile(
        r'^\s*(?P<book>(?:[1234]\s+)?[a-zA-Z\s]+?)\s*'
        r'(?:(?P<chapter>\d+)'
        r'(?:\s*:\s*(?P<start_verse>\d+)'
        r'(?:\s*-\s*(?P<end_verse>\d+))?)?)?\s*$'
    )

    # Stricter pattern for finding references inside text
    EXTRACT_PATTERN = re.compile(
        r'(?P<book>(?:[1234]\s+)?[A-Z][a-zA-Z\s]+?)\s+'
        r'(?P<chapter>\d+)'
        r'(?:\s*:\s*(?P<start_verse>\d+)'
        r'(?:\s*-\s*(?P<end_verse>\d+))?)?'
    )

    BOOK_ALIASES = {
        "gen": "Genesis", "ex": "Exodus", "exod": "Exodus", "lev": "Leviticus",
        "num": "Numbers", "deut": "Deuteronomy", "dt": "Deuteronomy",
        "josh": "Joshua", "judg": "Judges", "ruth": "Ruth",
        "1 sam": "1 Samuel", "2 sam": "2 Samuel",
        "1 kgs": "1 Kings", "2 kgs": "2 Kings",
        "1 chr": "1 Chronicles", "2 chr": "2 Chronicles",
        "ezra": "Ezra", "neh": "Nehemiah", "est": "Esther", "esth": "Esther",
        "job": "Job", "ps": "Psalms", "psalm": "Psalms", "psalms": "Psalms",
        "prov": "Proverbs", "eccl": "Ecclesiastes", "song": "Song of Solomon",
        "song of solomon": "Song of Solomon", "song of songs": "Song of Solomon",
        "isa": "Isaiah", "jer": "Jeremiah", "lam": "Lamentations",
        "ezek": "Ezekiel", "dan": "Daniel", "hos": "Hosea", "joel": "Joel",
        "amos": "Amos", "obad": "Obadiah", "jon": "Jonah", "jonah": "Jonah",
        "mic": "Micah", "nah": "Nahum", "hab": "Habakkuk", "zeph": "Zephaniah",
        "hag": "Haggai", "zech": "Zechariah", "mal": "Malachi",
        "matt": "Matthew", "mt": "Matthew", "mk": "Mark", "mark": "Mark",
        "lk": "Luke", "luke": "Luke", "jn": "John", "john": "John",
        "acts": "Acts", "rom": "Romans", "1 cor": "1 Corinthians",
        "2 cor": "2 Corinthians", "gal": "Galatians", "eph": "Ephesians",
        "phil": "Philippians", "col": "Colossians", "1 thess": "1 Thessalonians",
        "2 thess": "2 Thessalonians", "1 tim": "1 Timothy", "2 tim": "2 Timothy",
        "titus": "Titus", "phlm": "Philemon", "heb": "Hebrews", "jas": "James",
        "1 pet": "1 Peter", "2 pet": "2 Peter", "1 jn": "1 John", "2 jn": "2 John",
        "3 jn": "3 John", "jude": "Jude", "rev": "Revelation",
        "revelation": "Revelation"
    }

    @classmethod
    def parse(cls, reference: str) -> Optional[ParsedReference]:
        match = cls.PATTERN.match(reference.strip())
        if not match:
            return None
            
        gd = match.groupdict()
        
        # Normalize book name
        raw_book = gd.get('book')
        if not raw_book:
            return None
            
        raw_book = raw_book.strip().lower()
        # Reduce multiple spaces to single
        raw_book = re.sub(r'\s+', ' ', raw_book)
        
        # Check alias or assume it's valid
        normalized_book = cls.BOOK_ALIASES.get(raw_book, raw_book.title())
        
        chapter = int(gd['chapter']) if gd.get('chapter') else None
        start_verse = int(gd['start_verse']) if gd.get('start_verse') else None
        end_verse = int(gd['end_verse']) if gd.get('end_verse') else None
        
        return ParsedReference(
            book=normalized_book,
            chapter=chapter,
            start_verse=start_verse,
            end_verse=end_verse
        )

    @classmethod
    def extract_all(cls, text: str) -> List[ParsedReference]:
        """Extracts all references from a block of text."""
        results = []
        for match in cls.EXTRACT_PATTERN.finditer(text):
            book_raw = match.group('book').strip()
            book_normalized = cls.BOOK_ALIASES.get(book_raw.lower(), book_raw)
            
            # Simple validation to avoid matching random words
            if book_normalized.lower() not in set(v.lower() for v in cls.BOOK_ALIASES.values()):
                if book_normalized.lower() not in cls.BOOK_ALIASES:
                    continue
                    
            try:
                chapter = int(match.group('chapter')) if match.group('chapter') else None
                start_verse = int(match.group('start_verse')) if match.group('start_verse') else None
                end_verse = int(match.group('end_verse')) if match.group('end_verse') else None
                
                results.append(ParsedReference(
                    book=book_normalized,
                    chapter=chapter,
                    start_verse=start_verse,
                    end_verse=end_verse
                ))
            except (ValueError, TypeError):
                continue
                
        return results
