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


from uuid import uuid4
from deps import get_current_user, reuseable_oauth
router = APIRouter(
    prefix="/story",
    tags=["story"],
    responses={404: {"description": "Not found"}},

)

