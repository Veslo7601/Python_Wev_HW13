from libgravatar import Gravatar
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from My_project.database.models import User
from My_project.schemas import UserModel

# async def get_user_by_email(email: str, db: AsyncSession) -> User:
#     """function get user using email"""
#     return db.query(User).filter(User.email == email).first()

async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """function to get user by email"""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def create_user(body: UserModel, db: AsyncSession) -> User:
    """function create new user"""
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """function update token"""
    user.refresh_token = token
    await db.commit()