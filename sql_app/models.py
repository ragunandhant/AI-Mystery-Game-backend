from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, Table, DateTime, Text, UniqueConstraint, Enum as SqlEnum
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator
from enum import Enum
import datetime

Base = declarative_base()

class RoleEnum(Enum):
    WITNESS = 'witness'
    SUSPECT = 'suspect'

# Custom UUID type for MySQL
class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

# Association table for many-to-many relationship between Stories and Characters
story_character_association = Table(
    'story_character_association',
    Base.metadata,
    Column('story_id', GUID(), ForeignKey('stories.id')),
    Column('character_id', GUID(), ForeignKey('characters.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    interactions = relationship('Interaction', back_populates='user')
    stories = relationship('Story', back_populates='user')

    UniqueConstraint('name', 'email')

class Story(Base):
    __tablename__ = 'stories'
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = Column(GUID(), ForeignKey('users.id'))
    
    user = relationship('User', back_populates='stories')
    crime_scenes = relationship('CrimeScene', back_populates='story')
    characters = relationship('Character', secondary=story_character_association, back_populates='stories')

class CrimeScene(Base):
    __tablename__ = 'crime_scenes'
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    location = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    story_id = Column(GUID(), ForeignKey('stories.id'))
    
    story = relationship('Story', back_populates='crime_scenes')

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    role = Column(String(200), nullable=False)  # witness or suspect
    description = Column(Text, nullable=False)
    designation = Column(SqlEnum(RoleEnum), nullable=False)
    
    stories = relationship('Story', secondary=story_character_association, back_populates='characters')
    interactions = relationship('Interaction', back_populates='character')

class Interaction(Base):
    __tablename__ = 'interactions'
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey('users.id'))
    character_id = Column(GUID(), ForeignKey('characters.id'))
    story_id = Column(GUID(), ForeignKey('stories.id'))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now)
    
    user = relationship('User', back_populates='interactions')
    character = relationship('Character', back_populates='interactions')
    story = relationship('Story', back_populates='interactions')
