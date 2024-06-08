from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from My_project.database.models import Contact, PhoneNumber, Email, User
from My_project.schemas import ContactModel, ContactUpdateModel

def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """function takes contacts by list"""
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    """function get contact by ID"""
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

def create_contact(body: ContactModel, user: User, db: AsyncSession) -> Contact:
    """function create new contact"""
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birthday=body.date_of_birthday,
        additional_data=body.additional_data,
        phone_numbers=[PhoneNumber(phone_number=phone.phone_number) for phone in body.phone_numbers],
        emails=[Email(email=email.email) for email in body.emails],
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(contact_id: int, body: ContactUpdateModel, user: User, db: Session) -> Optional[Contact]:
    """function update contact"""
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        if body.first_name is not None:
            contact.first_name = body.first_name
        if body.last_name is not None:
            contact.last_name = body.last_name
        if body.date_of_birthday is not None:
            contact.date_of_birthday = body.date_of_birthday
        if body.additional_data is not None:
            contact.additional_data = body.additional_data

        db.query(PhoneNumber).filter(PhoneNumber.contact_id == contact.id).delete()
        for phone in body.phone_numbers:
            new_phone_number = PhoneNumber(phone_number=phone.phone_number, contact_id=contact.id)
            db.add(new_phone_number)

        db.query(Email).filter(Email.contact_id == contact.id).delete()
        for email in body.emails:
            new_email = Email(email=email.email, contact_id=contact.id)
            db.add(new_email)

        db.commit()
        db.refresh(contact)

    return contact

def remove_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    """function delete contact"""
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
