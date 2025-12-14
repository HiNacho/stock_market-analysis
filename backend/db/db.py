import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Base

DB_URL = os.getenv("DATABASE_URL", "sqlite:///stock-app.db")

def get_engine():
    return create_engine(DB_URL, echo=False, future=True)

def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
