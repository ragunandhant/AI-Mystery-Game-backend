from fastapi import APIRouter, Depends, HTTPException, status
from utils import get_db
from sqlalchemy.orm import Session
import sql_app.schemas as schemas
import sql_app.curd as curd
from validator_collection import validators
import uuid
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sql_app.schemas import  TokenSchema,SystemUser

from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
)
from uuid import uuid4
from deps import get_current_user, reuseable_oauth
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},

)

@router.post("/signup",status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validators.email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    users = curd.create_user(db, user)
    
    return {"name": users.name, "email": users.email, "is_active": users.is_active}



@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = curd.get_user_by_name(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    
    if user.hashed_password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }



@router.get("/get_user/{user_id}",status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(user_id: uuid.UUID, currentUser = Depends(get_current_user), db: Session = Depends(get_db)):

    user = curd.get_user(db, user_id)
    user = schemas.UserOut(id=user.id, username=user.name, email=user.email)
    

@router.get('/me', summary='Get details of currently logged in user')
async def get_me(user = Depends(get_current_user)):
    return user
