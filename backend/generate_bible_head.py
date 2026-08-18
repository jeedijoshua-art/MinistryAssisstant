import os

init_path = "app/models/__init__.py"
with open(init_path, "r") as f:
    no_bible_init = f.read()

all_models = """from app.models.domain import (
    Base, Church, Pastor, Conversation, Message, Sermon, SermonSection, SermonHistory,
    SermonTemplate, SermonTag, SermonTagsLink, SermonReference, BibleCharacter,
    BibleVersion, VerseHistory, Preferences, PromptHistory, AIUsage, BibleTranslation,
    BibleBook, BibleChapter, BibleVerse, CrossReference, BibleTopic, TopicVerse,
    CharacterReference, BookSummary, ChapterSummary, VerseNotes, BrandProfile,
    AssetFolder, AssetTag, AssetTagsLink, CreativeProject, CreativeAsset,
    CommunicationProject, CommunicationAsset, User, Role, Permission, AuditLog, Devotional, Prayer
)
"""

# 1. Wipe DB
os.system("PYTHONPATH=. .venv/bin/python wipe_db.py")

# 2. Create tables using current __init__.py (no Bible models)
create_script = """
from sqlalchemy import create_engine
from app.config import get_settings
from app.models.domain import Base
import app.models

engine = create_engine(get_settings().database_url)
Base.metadata.create_all(bind=engine)
print("Created tables without Bible models.")
"""
with open("create_partial.py", "w") as f:
    f.write(create_script)

os.system("PYTHONPATH=. .venv/bin/python create_partial.py")

# 3. Stamp HEAD
os.system("PYTHONPATH=. .venv/bin/alembic stamp head")

# 4. Write ALL models to __init__.py
with open(init_path, "w") as f:
    f.write(all_models)

# 5. Autogenerate migration at HEAD
os.system("PYTHONPATH=. .venv/bin/alembic revision --autogenerate -m 'Add Bible tables'")

print("Successfully generated migration at HEAD!")
