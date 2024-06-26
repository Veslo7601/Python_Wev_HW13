from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_limiter.depends import RateLimiter

from My_project.database.database import async_get_database
from My_project.database.models import User
from My_project.services.auth import (create_access_token, create_refresh_token,
                                      get_email_from_refresh_token, get_current_user, Hash,
                                      get_email_from_token)
from My_project.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from My_project.repository import users as repository_users

from My_project.services.email import send_email

router = APIRouter(prefix="/authentication")
hash = Hash()
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             description="No more than 10 requests per minute",
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(async_get_database)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = hash.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    background_tasks.add_task(send_email,
                              new_user.email,
                              new_user.username,
                              str(request.base_url))

    return {
        "username": new_user.username,
        "email": new_user.email,
        "avatar": new_user.avatar,
        "detail": "User successfully created. Check your email for confirmation."
    }

@router.post("/login", response_model=TokenModel,
             description="No more than 10 requests per minute",
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(async_get_database)):
    user_exist = await repository_users.get_user_by_email(body.username, db)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash.verify_password(body.password, user_exist.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    if not user_exist.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    
    access_token = await create_access_token(data={"sub": user_exist.email})
    refresh_token = await create_refresh_token(data={"sub": user_exist.email})
    await repository_users.update_token(user_exist, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}',
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def confirmed_email(token: str, db: AsyncSession = Depends(async_get_database)):
    email = await get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

@router.post('/request_email',
             description="No more than 10 requests per minute",
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(async_get_database)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email,
                            user.email,
                            user.username,
                            request.base_url)
    return {"message": "Check your email for confirmation"}


@router.get('/refresh_token', response_model=TokenModel,
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(async_get_database)):
    token = credentials.credentials
    email = await get_email_from_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await create_access_token(data={"sub": email})
    refresh_token = await create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}
