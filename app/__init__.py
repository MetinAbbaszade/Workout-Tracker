from sqlmodel import SQLModel
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.api.v1.endpoints.auth import router as auth_router


MYSQL_LINK = 'mysql+pymysql://root:M3tin190534@localhost/WorkOut'
app = FastAPI()
engine = create_engine(url=MYSQL_LINK)

def create_app():
    app.include_router(auth_router)

    return app

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)