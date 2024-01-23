from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

from dotenv import dotenv_values, load_dotenv
load_dotenv(override=False)
environment = dotenv_values(".env")

dbname = environment["DB_NAME"]
user = environment["DB_USER"]
password = environment["DB_PASSWORD"]
host = environment["DB_HOST"]
port = environment["DB_PORT"]



logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}', echo=True)


Session = sessionmaker(bind=engine)

Base = declarative_base()