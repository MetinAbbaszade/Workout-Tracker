from app.persistence.abstract import IRepository
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


class MemoryRepository(IRepository):

    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        return session.execute(select(self.model)).scalars().all()


    async def get(self, obj_id, session: AsyncSession):
        try:
            if isinstance(obj_id, str):
                obj_id = UUID(obj_id)
            else:
                pass
        except:
            raise ValueError('Value not suitable for UUID')
        
        data = session.execute(select(self.model).where(self.model.id == obj_id))

        return data.scalars().first()

    async def add(self, obj, session: AsyncSession):
        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj


    async def update(self, obj, obj_id, session: AsyncSession):
        existing_data = await self.get(obj_id=obj_id, session=session)

        for key, value in obj:
            if existing_data[key] != obj[key]:
                setattr(existing_data, key, value)

        session.commit()
        session.refresh(existing_data)
        return existing_data


    async def delete(self, obj_id, session: AsyncSession):
        existing_data = await self.get(obj_id=obj_id, session=session)

        session.delete(existing_data)
        session.commit()

        return None
