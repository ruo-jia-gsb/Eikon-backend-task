import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL, echo = True)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative.declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally:
        db.close()

def get_connection():
    db = engine.connect()
    try: 
        yield db 
    finally:
        db.close()
