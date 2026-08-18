from sqlalchemy import text
from sqlalchemy import create_engine
import os

import os
from sqlalchemy import create_engine

# try to get sync engine
url = os.getenv("DATABASE_URL")
if not url:
    print("No DATABASE_URL in env, trying to load from .env")
    from dotenv import load_dotenv
    load_dotenv()
    url = os.getenv("DATABASE_URL")

print(f"URL: {url}")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://")

engine = create_engine(url)

tables = [
    'sermon_tags_link',
    'sermon_references',
    'sermon_history',
    'sermon_sections',
    'sermon_tags',
    'sermon_templates'
]

with engine.begin() as conn:
    for table in tables:
        print(f"Dropping {table}...")
        conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))

print("Done!")
