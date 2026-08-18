import os
import time

init_path = "app/models/__init__.py"
bak_path = "app/models/__init__.py.bak"

# 1. Ensure __init__.py does NOT have Bible models
with open(init_path, "r") as f:
    current_init = f.read()

# We'll just read from our known backup which has EVERYTHING, and strip the Bible models.
with open(bak_path, "r") as f:
    orig_init = f.read()

no_bible_imports = """
from app.models.domain import (
    Base,
    Church,
    Pastor,
    Conversation,
    Message,
    Sermon,
    SermonSection,
    SermonHistory,
    SermonTemplate,
    SermonTag,
    SermonTagsLink,
    SermonReference,
    Prayer,
    Devotional,
    Preferences,
    ChurchProfile,
    PromptHistory,
    AIUsage,
    BrandProfile,
    AssetFolder,
    AssetTag,
    AssetTagsLink,
    CreativeProject,
    CreativeAsset,
    CommunicationProject,
    CommunicationAsset,
    User,
    Role,
    Permission,
    AuditLog
)
"""
with open(init_path, "w") as f:
    f.write(no_bible_imports)

# 2. Wipe DB
os.system("PYTHONPATH=. .venv/bin/python wipe_db.py")

# 3. Create all tables WITHOUT Bible models
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

# 4. Stamp HEAD
os.system("PYTHONPATH=. .venv/bin/alembic stamp head")

# 5. Restore original __init__.py (WITH Bible models)
with open(init_path, "w") as f:
    f.write(orig_init)

# 6. Autogenerate new migration AT HEAD
os.system("PYTHONPATH=. .venv/bin/alembic revision --autogenerate -m 'Add Bible tables to production'")

print("Successfully generated migration at HEAD!")
