from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date

Base = declarative_base()

class PhoneNumber(Base):
    """Class for phone number"""
    __tablename__ = "phone_numbers"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(15), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    contact = relationship("Contact", back_populates="phone_numbers")

class Email(Base):
    """Class for email"""
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    contact = relationship("Contact", back_populates="emails")

class Contact(Base):
    """Class for contact"""
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    date_of_birthday = Column(Date, nullable=True)
    additional_data = Column(String(256), nullable=True)
    phone_numbers = relationship("PhoneNumber", back_populates="contact", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="contact", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="contacts")

class User(Base):
    """Class for users"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")