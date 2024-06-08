from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class PhoneNumberModel(BaseModel):
    """Base model for phone number"""
    phone_number: str = Field(max_length=15)


class PhoneNumberResponse(PhoneNumberModel):
    """Response model for phone number"""
    id: int

    class Config:
        orm_mode = True


class EmailModel(BaseModel):
    """Base model for email"""
    email: str = Field(max_length=128)


class EmailResponse(EmailModel):
    """Response model for email"""
    id: int

    class Config:
        orm_mode = True


class ContactModel(BaseModel):
    """Base model for contact"""
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    date_of_birthday: date
    additional_data: Optional[str] = Field(max_length=256, default=None)
    phone_numbers: List[PhoneNumberModel]
    emails: List[EmailModel]


class ContactUpdateModel(BaseModel):
    """Base model for update contact"""
    first_name: Optional[str] = Field(max_length=64)
    last_name: Optional[str] = Field(max_length=64)
    date_of_birthday: Optional[date]
    additional_data: Optional[str] = Field(max_length=256, default=None)
    phone_numbers: List[PhoneNumberModel]
    emails: List[EmailModel]


class ContactResponse(ContactModel):
    """Response model for contact"""
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    """Base model for user"""
    username: str = Field(max_length=64)
    email: str = Field(max_length=256)
    password: str = Field(min_length=8, max_length=255)

class UserDBModel(BaseModel):
    """Base model for user in database"""
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    """Response model for user"""
    username: str
    email: str
    avatar: str
    detail: str = "User successfully created"

    class Config:
        orm_mode = True

class TokenModel(BaseModel):
    """Base model for token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
