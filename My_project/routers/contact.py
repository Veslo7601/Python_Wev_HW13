from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from My_project.database.database import get_database
from My_project.schemas import ContactModel, ContactResponse
from My_project.repository import contact as repository_contact
from My_project.database.models import User
from My_project.services.auth import get_current_user

router = APIRouter(prefix="/contact")

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0,
                        limit: int = 100,
                        db: Session = Depends(get_database),
                        current_user: User = Depends(get_current_user)):
    contacts = repository_contact.get_contacts(skip, limit, current_user, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int,
                       db: Session = Depends(get_database),
                       current_user: User = Depends(get_current_user)):
    contact = repository_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    contact = repository_contact.create_contact(body, current_user, db)
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel,
                         contact_id: int,
                         db: Session = Depends(get_database),
                         current_user: User = Depends(get_current_user)):
    contact = repository_contact.update_contact(contact_id, current_user, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=dict)
async def remove_contact(contact_id: int,
                         db: Session = Depends(get_database),
                         current_user: User = Depends(get_current_user)):
    contact = repository_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"detail": "Contact successfully deleted"}
