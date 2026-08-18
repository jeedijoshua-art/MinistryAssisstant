import os
import glob
import ast

# 1. Rewrite __init__.py to only import Bible models
init_path = "app/models/__init__.py"
with open(init_path, "r") as f:
    orig_init = f.read()

bible_imports = """
from app.models.domain import (
    Base,
    BibleCharacter,
    BibleVersion,
    VerseHistory,
    BibleTranslation,
    BibleBook,
    BibleChapter,
    BibleVerse,
    CrossReference,
    BibleTopic,
    TopicVerse,
    CharacterReference,
    BookSummary,
    ChapterSummary,
    VerseNotes
)
"""
with open(init_path, "w") as f:
    f.write(bible_imports)

# 2. Wipe DB and Stamp HEAD
os.system("PYTHONPATH=. .venv/bin/python wipe_db.py")
os.system("PYTHONPATH=. .venv/bin/alembic stamp head")

# 3. Autogenerate migration
os.system("PYTHONPATH=. .venv/bin/alembic revision --autogenerate -m 'temp_bible'")

# 4. Restore __init__.py
with open(init_path, "w") as f:
    f.write(orig_init)

# 5. Find the newly generated migration
files = glob.glob("alembic/versions/*_temp_bible.py")
if not files:
    print("Failed to generate migration")
    exit(1)
temp_file = files[0]

with open(temp_file, "r") as f:
    temp_content = f.read()

# 6. Extract upgrade and downgrade functions
upgrade_str = temp_content.split("def upgrade() -> None:")[1].split("def downgrade() -> None:")[0]
downgrade_str = temp_content.split("def downgrade() -> None:")[1]

# 7. Inject into b688031139ce
target_file = "alembic/versions/b688031139ce_add_bible_engine_models.py"
with open(target_file, "r") as f:
    target_content = f.read()

# Replace the pass in upgrade and downgrade
part1 = target_content.split("def upgrade() -> None:")[0]

new_content = part1 + "def upgrade() -> None:" + upgrade_str + "def downgrade() -> None:" + downgrade_str

# make sure postgresql dialect is imported in b688031139ce
if "from sqlalchemy.dialects import postgresql" not in new_content:
    new_content = new_content.replace("import sqlalchemy as sa", "import sqlalchemy as sa\nfrom sqlalchemy.dialects import postgresql")

with open(target_file, "w") as f:
    f.write(new_content)

# 8. Delete temp migration
os.remove(temp_file)
print("Successfully populated b688031139ce!")
