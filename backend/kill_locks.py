import os
from sqlalchemy import create_engine, text

url = os.getenv("DATABASE_URL")
if not url:
    from dotenv import load_dotenv
    load_dotenv()
    url = os.getenv("DATABASE_URL")

if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://")

engine = create_engine(url, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    print("Terminating active queries...")
    conn.execute(text("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE state = 'active'
        AND pid <> pg_backend_pid();
    """))
    print("Locks cleared!")
