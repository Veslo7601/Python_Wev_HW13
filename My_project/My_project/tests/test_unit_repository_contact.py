import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import MagicMock, AsyncMock

from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from My_project.database.models import Contact, PhoneNumber, Email, User
from My_project.schemas import ContactCreate, ContactUpdate
from My_project.repository.contact import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
)


class AsyncMockUser:
    def __init__(self, id):
        self.id = id

    async def __call__(self):
        return self

class TestContact(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = AsyncMockUser(id=1)

    # async def test_get_contacts(self):
    #     contacts = [Contact()]

    #     # Create a mock for the result of `execute`
    #     mock_result = AsyncMock()
    #     mock_result.fetchall.return_value = contacts

    #     # Configure the session's execute method to return our mock result
    #     self.session.execute = AsyncMock(return_value=mock_result)
        
    #     # Call the async function and await the result
    #     result = await get_contacts(skip=0, limit=10, user=self.user(), db=self.session)
        
    #     # Assert that the result matches the expected contacts
    #     self.assertEqual(result, contacts)


    async def test_get_contact_not_found(self):
        # Configure the mock result to return None (simulating not found)
        mock_result = AsyncMock()
        mock_result.fetchone.return_value = None
        self.session.execute.return_value = mock_result

        # Call the async function and await the result
        result = await get_contact(1, user=self.user(), db=self.session)

        # Assert that the result is None
        self.assertIsNone(result)
if __name__ == '__main__':
    unittest.main()
