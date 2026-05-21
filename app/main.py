from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import engine, Base
from app.routers import auth, users, campaigns, characters

#importa os models para as tabelas serem criadas no banco
from app.models import user, campaign, character  # noqa

#cria as tabelas que ainda não existem no banco
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #retorna erros de validação
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Dados inválidos.",
            "errors": exc.errors()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #retorna erros de validação de forma correta
    errors = []
    for error in exc.errors():
        errors.append({
            "campo": str(error.get("loc", "")),
            "mensagem": error.get("msg", "")
        })
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Dados inválidos.",
            "errors": errors
        }
    )


#registra os routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(characters.router)


@app.get("/", tags=["Home"])
def raiz():
    return {
        "status": "online",
        "mensagem": "Bem-vindo à API de RPG de Mesa!",
        "docs": "http://localhost:8000/docs"
    }
