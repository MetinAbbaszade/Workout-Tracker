from datetime import datetime
from pydantic import BaseModel
from fastapi import Form, Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.extensions import get_db
from app.service import facade
from app.models.users import User

SECRETKEY = 'superincrediblesupersupermyexcellentandandandandandandnadsimplekey'
token = HTTPBearer()

class AuthResponse(BaseModel):
    message: str
    token: str

class userModel(BaseModel):
    id: UUID | None = None
    name: str
    surname: str
    email: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None



class customFormDataOAuthentication:
    def __init__(
            self,
            email: str = Form(...),
            password: str = Form(...)
    ):
        self.email = email
        self.password = password

async def create_access_token(payload):
    for key, value in payload.items():
        if isinstance(value, UUID):
            payload[key] = str(value)
    access_token = jwt.encode(
        payload=payload,
        key=SECRETKEY,
        algorithm='HS256'
    )
    return access_token

async def decode_token(token):
    decoded_token = jwt.decode(
        jwt=token,
        key=SECRETKEY,
        algorithms=['HS256']
    )
    return decoded_token


async def get_token_from_credentials(token: str = Depends(token)):
    return token.credentials

async def get_current_user(token: str = Depends(get_token_from_credentials), db : AsyncSession = Depends(get_db)):
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token.get('sub')
        user: User = await facade.get_user(user_id=user_id, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found'
            )
        return user
    except Exception as e:
        return {'Error': e}