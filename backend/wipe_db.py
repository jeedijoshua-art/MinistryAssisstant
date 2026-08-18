from sqlalchemy import create_engine, MetaData
from app.config import get_settings

engine = create_engine(get_settings().database_url)
meta = MetaData()
meta.reflect(bind=engine)
meta.drop_all(bind=engine)
print("All tables dropped.")
