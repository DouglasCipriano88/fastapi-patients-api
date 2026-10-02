from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///patients.db"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
