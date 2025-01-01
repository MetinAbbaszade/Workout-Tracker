from app.models.basemodel import BaseModel
import re
from sqlmodel import Field
from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'])

class User(BaseModel, table=True):
    name: str = Field(description='Name of User')
    surname: str = Field(description='Surname of User')
    email: str = Field(description='Email of User')
    password: str = Field(description='Password of User')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', kwargs['email'])

        if valid:
            self.email = kwargs['email']
        else:
            ValueError('Email is on discorrect Format')
        
        if 'password' in kwargs:
            self.password = self.hash_password(kwargs['password'])

    @staticmethod
    def hash_password(password):
        return context.hash(password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return context.verify(plain_password, hashed_password)
    
    def to_dict(self):
        dictionary = super().to_dict()

        dictionary.update({
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'password': self.password
        })