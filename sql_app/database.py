from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
load_dotenv()
password = os.getenv("password")
engine = create_engine("mysql://root:%s@localhost:3306/mysterygamedb" % quote_plus(password))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
