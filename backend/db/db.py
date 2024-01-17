import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging


# dbname = os.environ.get('DB_NAME')
dbname = 'postgres'
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
# host = os.environ.get('DB_HOST')
host = 'localhost'
port = os.environ.get('DB_PORT')


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}', echo=True)


Session = sessionmaker(bind=engine)

Base = declarative_base()