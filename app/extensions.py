def get_db():
    from app import engine
    from sqlalchemy.orm import sessionmaker

    sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    db = sessionLocal()

    try:
        yield db
    except:
        db.close()