from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    async def get_all(self, session):
        ...

    @abstractmethod
    async def get(self, obj_id, session):

        ...
    @abstractmethod
    async def add(self, obj, session):
        ...

    @abstractmethod
    async def update(self, obj, obj_id, session):
        ...

    @abstractmethod
    async def delete(self, obj_id, session):
        ...