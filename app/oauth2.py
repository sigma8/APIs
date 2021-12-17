from re import S
from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "TOBESET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_be_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_be_encode.update({"exp": expire})
    jwt_encode = jwt.encode(to_be_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.encode(token=SECRET_KEY, algorithm=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"No se pudieron validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
