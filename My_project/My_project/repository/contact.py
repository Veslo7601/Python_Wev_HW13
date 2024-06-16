from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from My_project.database.models import Contact, PhoneNumber, Email, User
from My_project.schemas import ContactCreate, ContactUpdate

async def get_contacts(skip: int, limit: int, user: User, db: AsyncSession) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    user_instance = await user
    user_id = user_instance.id
    query = select(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    contacts = await result.scalars().all()
    return contacts

async def get_contact(contact_id: int, user: User, db: AsyncSession) -> Optional[Contact]:
    """
    Retrieves a specific contact by ID for a given user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The contact if found, otherwise None.
    :rtype: Optional[Contact]
    """
    user_instance = await user
    user_id = user_instance.id

    query = select(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user_id))
    result = await db.execute(query)
    contact = result.scalar()
    return contact

async def create_contact(body: ContactCreate, user: User, db: AsyncSession) -> Contact:
    """
    Creates a new contact for a given user.

    :param body: The details of the contact to create.
    :type body: ContactCreate
    :param user: The user for whom the contact is being created.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created contact.
    :rtype: Contact
    """
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
    """
    Updates an existing contact for a given user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The new details of the contact.
    :type body: ContactUpdate
    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated contact if found, otherwise None.
    :rtype: Optional[Contact]
    """
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
    """
    Deletes a specific contact for a given user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The deleted contact if found, otherwise None.
    :rtype: Optional[Contact]
    """
    contact = await get_contact(contact_id, user, db)
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
