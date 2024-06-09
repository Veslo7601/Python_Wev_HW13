from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from My_project.database.database import async_get_database
from My_project.schemas import ContactCreate, ContactResponse
from My_project.repository import contact as repository_contact
from My_project.database.models import User
from My_project.services.auth import get_current_user

router = APIRouter(prefix="/contact")

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0,
                        limit: int = 100,
                        db: AsyncSession = Depends(async_get_database),
                        current_user: User = Depends(get_current_user)):
    contacts = await repository_contact.get_contacts(skip, limit, current_user, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int,
                       db: AsyncSession = Depends(async_get_database),
                       current_user: User = Depends(get_current_user)):
    contact = await repository_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse)
async def create_contact(
    body: ContactCreate,
    db: AsyncSession = Depends(async_get_database),
    current_user: User = Depends(get_current_user)
):
    return await repository_contact.create_contact(body, current_user, db)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int,
                         body: ContactCreate,
                         db: AsyncSession = Depends(async_get_database),
                         current_user: User = Depends(get_current_user)):
    contact = await repository_contact.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=dict)
async def remove_contact(contact_id: int,
                         db: AsyncSession = Depends(async_get_database),
                         current_user: User = Depends(get_current_user)):
    contact = await repository_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"detail": "Contact successfully deleted"}
