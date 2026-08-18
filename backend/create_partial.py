
from sqlalchemy import create_engine
from app.config import get_settings
from app.models.domain import Base
import app.models

engine = create_engine(get_settings().database_url)
Base.metadata.create_all(bind=engine)
print("Created tables without Bible models.")
