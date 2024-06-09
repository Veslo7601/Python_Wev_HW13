from typing import List, Optional
from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import and_

from My_project.database.models import Contact, PhoneNumber, Email, User
from My_project.schemas import ContactCreate, ContactUpdate

async def get_contacts(skip: int, limit: int, user: User, db: AsyncSession) -> List[Contact]:
    """function takes contacts by list"""
    user_instance = await user
    user_id = user_instance.id
    query = select(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts

async def get_contact(contact_id: int, user: User, db: AsyncSession) -> Optional[Contact]:
    """function get contact by ID"""

    user_instance = await user
    user_id = user_instance.id

    query = select(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user_id))
    result = await db.execute(query)
    contact = result.scalars().first()
    return contact

async def create_contact(body: ContactCreate, user: User, db: AsyncSession) -> Contact:
    """function create new contact"""
    user_instance = await user
    user_id = user_instance.id
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birthday=body.date_of_birthday,
        additional_data=body.additional_data,
        phone_numbers=[PhoneNumber(phone_number=phone.phone_number) for phone in body.phone_numbers],
        emails=[Email(email=email.email) for email in body.emails],
        user_id=user_id
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: AsyncSession) -> Optional[Contact]:
    """function update contact"""
    contact = await get_contact(contact_id, user, db)
    if contact:
        if body.first_name is not None:
            contact.first_name = body.first_name
        if body.last_name is not None:
            contact.last_name = body.last_name
        if body.date_of_birthday is not None:
            contact.date_of_birthday = body.date_of_birthday
        if body.additional_data is not None:
            contact.additional_data = body.additional_data

        phone_number = select(PhoneNumber).filter(PhoneNumber.contact_id == contact.id)
        result = await db.execute(phone_number)
        result = result.scalars().first()
        await db.delete(result)

        for phone in body.phone_numbers:
            new_phone_number = PhoneNumber(phone_number=phone.phone_number, contact_id=contact.id)
            db.add(new_phone_number)

        email_db = select(Email).filter(Email.contact_id == contact.id)
        result = await db.execute(email_db)
        result = result.scalars().first()
        await db.delete(result)

        for email in body.emails:
            new_email = Email(email=email.email, contact_id=contact.id)
            db.add(new_email)

        await db.commit()
        await db.refresh(contact)


    return contact

async def remove_contact(contact_id: int, user: User, db: AsyncSession) -> Optional[Contact]:
    """function delete contact"""
    contact = await get_contact(contact_id, user, db)
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact