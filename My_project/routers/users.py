from typing import List
from os import environ
from fastapi import APIRouter, Depends, UploadFile, File
#from fastapi_limiter.depends import RateLimiter
import cloudinary
import cloudinary.uploader

from sqlalchemy.ext.asyncio import AsyncSession

from My_project.database.database import async_get_database
from My_project.database.models import User
from My_project.repository import users as repository_users
from My_project.services.auth import get_current_user
from My_project.schemas import UserDBModel

router = APIRouter(prefix="/users")

@router.get("/me/", response_model=UserDBModel)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """function read user"""
    return current_user

@router.patch("/avatar", response_model=UserDBModel)
async def update_avatar_user(file: UploadFile = File(),
                             current_user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(async_get_database)):
    """function update avatar"""
    cloudinary.config(
        cloud_name=environ.get("CLOUDINARY_NAME"),
        api_key=environ.get("CLOUDINARY_API_KEY"),
        api_secret=environ.get("CLOUDINARY_API_SECRET"),
        secure=True
    )
    result = cloudinary.uploader.upload(file.file,
                                        public_id=f'My_project/{current_user.username}',
                                        overwrite=True)
    url = cloudinary.CloudinaryImage(f'My_project/{current_user.username}').build_url(width=250, height=250, crop='fill', version=result.get('version'))
    user = await repository_users.update_avatar(current_user.email, url, db)
    return user