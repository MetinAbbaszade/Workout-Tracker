from app.persistence.repository import MemoryRepository 
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

class Facade:
    def __init__(self):
        self.user_repo = MemoryRepository(User)

    async def get_all_users(self, db: AsyncSession):
        return await self.user_repo.get_all(session=db)
    
    async def get_user(self, user_id, db: AsyncSession):
        return await self.user_repo.get(obj_id=user_id, session=db)
    
    async def add_user(self, user, db: AsyncSession):
        data = user.dict()
        new_user = User(**data)

        await self.user_repo.add(obj=new_user, session=db)
        return  new_user
    
    async def update_user(self, user_id, user_data, db: AsyncSession):
        data = user_data.dict()
        return await self.user_repo.update(obj=user_data, obj_id=user_id, session=db)


    async def delete_user(self, user_id, db: AsyncSession):
        return await self.user_repo.delete(obj_id=user_id, session=db)
    
    async def get_user_by_email(self, email, db: AsyncSession):
        users = await self.user_repo.get_all(session=db)
        return next((user for user in users if user.email == email), None)