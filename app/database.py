from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

DBpath = os.getenv("MY_DB_URL")

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessioinlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

base=declarative_base()

def get_db():
    db =sessioinlocal()
    try:
        yield db
    finally:
        db.close()