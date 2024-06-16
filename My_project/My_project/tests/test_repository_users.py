import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from My_project.repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar


import pytest
from unittest.mock import AsyncMock, MagicMock
from libgravatar import Gravatar

from My_project.database.models import User
from My_project.schemas import UserModel

@pytest.fixture
def user_model():
    return UserModel(email="test@example.com", username="Test User", password="password123")

@pytest.fixture
def user():
    return User(id=1, email="test@example.com", username="Test User", password="password123", avatar="http://example.com/avatar.png")

@pytest.fixture
def db_session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session

@pytest.mark.asyncio
async def test_get_user_by_email(user, db_session):
    db_session.execute.return_value.scalars.return_value.first.return_value = user
    result = await get_user_by_email("test@example.com", db_session)
    assert result == user
    db_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_user(user_model, db_session):
    avatar_url = "http://example.com/avatar.png"
    Gravatar.get_image = MagicMock(return_value=avatar_url)
    db_session.commit = AsyncMock()
    db_session.refresh = AsyncMock()
    new_user = await create_user(user_model, db_session)
    assert new_user.avatar == avatar_url
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_update_token(user, db_session):
    token = "new_refresh_token"
    await update_token(user, token, db_session)
    assert user.refresh_token == token
    db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_confirmed_email(user, db_session):
    db_session.execute.return_value.scalars.return_value.first.return_value = user
    await confirmed_email("test@example.com", db_session)
    assert user.confirmed is True
    db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_avatar(user, db_session):
    new_avatar_url = "http://example.com/new_avatar.png"
    db_session.execute.return_value.scalars.return_value.first.return_value = user
    updated_user = await update_avatar("test@example.com", new_avatar_url, db_session)
    assert updated_user.avatar == new_avatar_url
    db_session.commit.assert_called_once()
