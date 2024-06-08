from libgravatar import Gravatar
from sqlalchemy.orm import Session
from My_project.database.models import User
from My_project.schemas import UserModel

async def get_user_by_email(email: str, db: Session) -> User:
    """function get user using email"""
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    """function create new user"""
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """function update token"""
    user.refresh_token = token
    db.commit()