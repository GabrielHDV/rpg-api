from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, campaigns, characters

# importa os models para as tabelas serem criadas no banco
from app.models import user, campaign, character  # noqa

# cria as tabelas que ainda não existem no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RPG de Mesa API",
    description="API para gerenciamento de campanhas e personagens de RPG de Mesa.",
    version="1.0.0",
)

#permite que frontends acessem a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#registra os routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(characters.router)


@app.get("/", tags=["Home"])
def raiz():
    "Verifica se a API está online."
    return {
        "status": "online",
        "mensagem": "Bem-vindo à API de RPG de Mesa!",
        "docs": "http://localhost:8000/docs"
    }
