from fastapi import FastAPI
from app.database import engine, Base

#importa os models para as tabelas serem criadas no banco
from app.models import user, campaign, character  # noqa

#cria as tabelas que ainda não existem no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="⚔️ RPG de Mesa API")


@app.get("/")
def raiz():
    return {
        "status": "online",
        "mensagem": "Bem-vindo à API de RPG de Mesa! 🐉",
        "docs": "http://localhost:8000/docs"
    }

