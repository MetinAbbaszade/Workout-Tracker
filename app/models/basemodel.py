from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    def update(self, object):
        for key, value in object:
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }