from db.models.models import Users
from db.db import Session
from passlib.context import CryptContext

from middlewares.auth import get_jwt_token

from dotenv import dotenv_values, load_dotenv
load_dotenv(override=False)
environment = dotenv_values(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_and_rehash_password(plain_password: str, hashed_password: str):
    password_matches = pwd_context.verify(plain_password, hashed_password)
    password_needs_rehash = pwd_context.needs_update(hashed_password)
    return password_matches, password_needs_rehash

def check_password_and_rehash_if_needed(username: str, plain_password: str):
    with Session() as session:
        user = session.query(Users).filter_by(name=username).first()
        if user is None:
            return False
        password_matches, password_needs_rehash = verify_and_rehash_password(plain_password, user.password)
        if password_matches and password_needs_rehash:
            user.password = hash_password(plain_password)
            session.commit()
        return password_matches


def new_user (username: str, password: str):
    try:
        
        with Session() as session:
            user = Users(name=username, password=hash_password(password))
            session.add(user)
            session.commit()
    except Exception as e:
        raise e

def login_get_token (username: str, password: str):
    try:
        password_matches = check_password_and_rehash_if_needed(username, password)
        logged= get_jwt_token(password_matches, username)
        return logged
    except Exception as e:
        raise e
