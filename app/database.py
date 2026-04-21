from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#cria a conexão com o banco
engine = create_engine(DATABASE_URL)

#cada requisição vai ter sua própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#todas as tabelas herdam daqui
Base = declarative_base()


def get_db():
    #abre a sessão e garante que fecha no final, mesmo se der erro
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
