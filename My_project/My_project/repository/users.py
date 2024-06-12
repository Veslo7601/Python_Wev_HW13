from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from My_project.database.models import User
from My_project.schemas import UserModel

async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their email address.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user if found, otherwise None.
    :rtype: User
    """
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def create_user(body: UserModel, db: AsyncSession) -> User:
    """
    Creates a new user with the provided details.

    :param body: The details of the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user.
    :rtype: User
    """
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
    """
    Updates the refresh token for a given user.

    :param user: The user whose token is to be updated.
    :type user: User
    :param token: The new refresh token.
    :type token: str | None
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user.refresh_token = token
    await db.commit()

async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirms the email address of a user.

    :param email: The email address to confirm.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar(email: str, url: str, db: AsyncSession) -> User:
    """
    Updates the avatar URL for a given user.

    :param email: The email address of the user.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    return user
