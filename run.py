from app import create_app, create_db_and_tables

if __name__ == "__main__":
    from uvicorn import run
    app = create_app()
    create_db_and_tables()
    run(app=app, host='0.0.0.0', port=8000)