import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

###################################
###### Map all env variables ######
###################################

DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
TABLE_NAME = os.environ.get("TABLE_NAME")

#Connect to postgres and create a database
def create_url(user = DB_USER, 
               host = DB_HOST, 
               pw = DB_PASSWORD, 
               port = "5432", 
               db_name = DB_NAME):
    
    url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db_name}"
    return url 

DATABASE_URL = create_url()

######################################
##### Create engine and sessions #####
######################################

engine = sql.create_engine(DATABASE_URL, echo = True)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = orm.declarative_base()

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
