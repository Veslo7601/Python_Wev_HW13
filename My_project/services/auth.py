from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from starlette import status

from My_project.database.database import async_get_database
from My_project.database.models import User
from My_project.repository.users import get_user_by_email


class Hash:
    """Class for hashing passwords"""
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """Verify the provided password against the stored hashed password"""
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """Generate a hash for the provided password"""
        return self.context.hash(password)


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """Create an access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "access_token"})
    encoded_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_access_token

async def create_refresh_token(data: dict, expires_delta: Optional[float] = None):
    """Create a refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now() + timedelta(days=7)

    to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "refresh_token"})
    encoded_refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_refresh_token

async def get_email_from_refresh_token(refresh_token: str):
    """Extract email from the provided refresh token"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == 'refresh_token':
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_get_database)):
    """Get the current user from the token"""
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == "access_token":
            email = payload.get("sub")
            if email is None:
                raise exception
        else:
            raise exception
    except JWTError:
        raise exception

    # user = db.query(User).filter(User.email == email).first()
    user = get_user_by_email(email, db)
    if user is None:
        raise exception
    return user

async def create_email_token(data: dict):
    """function create email-token"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=7)
    to_encode.update({"iat": datetime.now(), "exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_email_from_token(token: str):
    """function get email from token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid token payload")
        return email
    except JWTError as e:
        print(f"{e}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid token for email verification")