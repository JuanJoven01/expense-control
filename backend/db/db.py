import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()