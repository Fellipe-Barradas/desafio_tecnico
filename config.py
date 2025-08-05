from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()
sqlite_path = os.getenv('SQLITE_CAMINHO', 'db.sqlite3')

database_url = f"sqlite:///{sqlite_path}"

# Criar engine síncronos
engine = create_engine(database_url, echo=False, pool_size=3, max_overflow=0)

# Funções síncronas para criar/deletar tabelas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
        
def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    
def get_session() -> Generator[Session, None, None]:
    session = sessionmaker(
        engine, class_=Session, expire_on_commit=False
    )()
    try:
        yield session
    finally:
        session.close()