from pathlib import Path
from sqlmodel import create_engine, SQLModel, Session

from app.services.csv_service import insert_csv_data

DATABASE_URL = 'sqlite:///db.sqlite'
CSV_DIR = Path("app/static/games.csv")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        insert_csv_data(CSV_DIR, session)
    
def get_session():
    with Session(engine) as session:
        yield session