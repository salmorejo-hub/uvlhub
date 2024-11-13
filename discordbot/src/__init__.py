# __init__.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from src.database.models import *
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASSWORD')}@{os.getenv('MARIADB_HOSTNAME')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_DATABASE')}"

engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

# Create database tables
Base.metadata.create_all(bind=engine)