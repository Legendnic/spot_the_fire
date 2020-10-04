from Models.pydantic_models import User_Pydantic, UserIn_Pydantic, Token, TokenData
from Models.models import Users

from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional, List
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi import Depends, HTTPException, Security, status
from pydantic import ValidationError

SECRET_KEY = 'a0f0ac7ef304a98add4507fd5902697f9788efb6be078aad2d198da8266e2487'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 120

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={"me": "only the current user can access full system."})

#hashing the password for registration of the user
def get_password_hash(password):
    return pwd_context.hash(password)

#verifying the password of the current login user
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#get user data equivalent to the current login user
async def get_user(Users, email:str):
    return await User_Pydantic.from_queryset_single(Users.get(email=email))

#authenticating the user
async def authenticate_user(Users, email:str, password:str):
    user = await get_user(Users, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#generate access token for user to use another url
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#get current user that has logged on into the system
async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else f'Bearer'
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": authenticate_value})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=email)
        # print("token_data:", token_data)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await get_user(Users, email=token_data.email)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions.", headers={"WWW-Authenticate":authenticate_value})

    return user
