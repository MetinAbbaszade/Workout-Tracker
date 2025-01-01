from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from app.api.v1.schemas.auth import userModel, customFormDataOAuthentication, create_access_token, AuthResponse
from app.extensions import get_db
from app.service import facade
from app.models.users import User
import pytest

router = APIRouter(prefix='/api/v1/auth', tags=['Authentication and Authorization'])

@router.post('/signup', response_model=userModel, status_code=status.HTTP_201_CREATED)
async def signup(user: userModel, db:AsyncSession = Depends(get_db)):
    email = user.email
    existing_user = await facade.get_user_by_email(email=email, db=db)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already Exists with this mail'
        )
    
    user.id = uuid4()
    user.created_at = datetime.now()
    user.updated_at = datetime.now()

    new_user = await facade.add_user(user=user, db=db)

    return new_user

@router.post('/login',response_model=str, status_code=status.HTTP_201_CREATED)
async def login(formdata: customFormDataOAuthentication = Depends(), db: AsyncSession = Depends(get_db)):
    email = formdata.email

    existing_user: User = await facade.get_user_by_email(email=email, db=db)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    password = formdata.password

    if not existing_user.verify_password(plain_password=password, hashed_password=existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='False Password'
        )
    
    payload = {
        'sub': existing_user.id,
        'email': existing_user.email,
        'name': existing_user.name,
        'surname': existing_user.surname
    }

    access_token = await create_access_token(payload=payload)
    print(access_token)
    return access_token