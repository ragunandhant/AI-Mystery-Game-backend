# sql_app/curd.py

from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
import uuid
def create_user(db: Session, user: UserCreate):
    print(user)
    db_user = User(name=user.name, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


#For story

from .models import Story
from .schemas import StoryCreate, StoryResponse

def create_story(db: Session, story: StoryCreate, user_id: uuid.UUID):
    db_story = Story(title = story.title,content = story.content, user_id=user_id)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def delete_story(db: Session, story_id: uuid.UUID):
    db_story = db.query(Story).filter(Story.id == story_id).first()
    db.delete(db_story)
    db.commit()
    return db_story
