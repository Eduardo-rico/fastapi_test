from passlib.context import CryptContext #libreria de encriptación
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import jwt
import time
from fastapi.security import OAuth2PasswordBearer
from models.jwt_user import JWTUser
from starlette.status import HTTP_401_UNAUTHORIZED

from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM


oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user_1 = {"username": "user_1", "password": "1233", "disabled": False, "role": "admin"}
fake_jwt_user_1 = JWTUser(**jwt_user_1)

pwd_context = CryptContext(schemes=["bcrypt"])

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_passwor)
    except Exception as e:
        return False

#Autenticar usuario y password para dar un token jwt
def authenticate_user(user: JWTUser):
    if fake_jwt_user_1.username == user.username:
        if verify_password(user.password, fake_jwt_user_1.password):
            user.role = "admin"
            return True
    return False

#crear un jwt de acceso
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username, "role": user.role, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    print(jwt_token)
    return jwt_token


#verificar si el jwt es correcto
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = payload.get("sub")
        expiration_time = payload.get("exp")
        role = payload.get('role')
        if time.time() < expiration_time:
            if fake_jwt_user_1.username == username:
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


def final_checks(username: str, role: str):
    #verificar el rol y cosas asi
    if role == "admin":
        return True
    else:
        return False