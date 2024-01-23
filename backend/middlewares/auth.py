from jose import jwt

from fastapi.security import HTTPBearer

from dotenv import dotenv_values, load_dotenv
load_dotenv(override=False)
environment = dotenv_values(".env")

def get_jwt_token(user_validated: bool, username: str):
    secret_key = environment["SECRET_KEY"]
    algorithm = environment["ALGORITHM"]
    body = {"user": username}
    if user_validated:
        return jwt.encode(body, secret_key, algorithm=algorithm)
    else:
        return False
    
def validate_jwt_token(token: str):
    secret_key = environment["SECRET_KEY"]
    algorithm = environment["ALGORITHM"]
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except:
        return False
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not validate_jwt_token(credentials.credentials):
                return False
            return credentials.credentials
        else:
            return False
    
