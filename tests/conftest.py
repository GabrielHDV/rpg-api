import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

#banco separado só para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    #cria as tabelas antes de cada teste e apaga depois
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    #substitui o banco real pelo banco de teste
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    #cria um admin e retorna o token
    client.post("/auth/register", json={
        "name": "Admin Teste",
        "email": "admin@teste.com",
        "password": "senha123",
        "role": "admin"
    })
    response = client.post("/auth/login", json={
        "email": "admin@teste.com",
        "password": "senha123"
    })
    return response.json()["access_token"]


@pytest.fixture
def player_token(client):
    #cria um player e retorna o token
    client.post("/auth/register", json={
        "name": "Player Teste",
        "email": "player@teste.com",
        "password": "senha123",
        "role": "player"
    })
    response = client.post("/auth/login", json={
        "email": "player@teste.com",
        "password": "senha123"
    })
    return response.json()["access_token"]
