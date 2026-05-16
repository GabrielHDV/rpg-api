def test_register_admin(client):
    #testa registro de um admin
    response = client.post("/auth/register", json={
        "name": "Gandalf",
        "email": "gandalf@rpg.com",
        "password": "senha123",
        "role": "admin"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "gandalf@rpg.com"
    assert data["role"] == "admin"
    assert "hashed_password" not in data


def test_register_player(client):
    #testa registro de um player
    response = client.post("/auth/register", json={
        "name": "Frodo",
        "email": "frodo@rpg.com",
        "password": "senha123",
        "role": "player"
    })
    assert response.status_code == 201
    assert response.json()["role"] == "player"


def test_register_email_duplicado(client):
    #não deve permitir dois usuários com o mesmo email
    client.post("/auth/register", json={
        "name": "Frodo",
        "email": "frodo@rpg.com",
        "password": "senha123",
        "role": "player"
    })
    response = client.post("/auth/register", json={
        "name": "Frodo 2",
        "email": "frodo@rpg.com",
        "password": "senha456",
        "role": "player"
    })
    assert response.status_code == 400


def test_login_sucesso(client):
    #testa login com credenciais corretas
    client.post("/auth/register", json={
        "name": "Gandalf",
        "email": "gandalf@rpg.com",
        "password": "senha123",
        "role": "admin"
    })
    response = client.post("/auth/login", json={
        "email": "gandalf@rpg.com",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_senha_errada(client):
    #testa login com senha incorreta
    client.post("/auth/register", json={
        "name": "Gandalf",
        "email": "gandalf@rpg.com",
        "password": "senha123",
        "role": "admin"
    })
    response = client.post("/auth/login", json={
        "email": "gandalf@rpg.com",
        "password": "senhaerrada"
    })
    assert response.status_code == 401


def test_login_email_inexistente(client):
    #testa login com email que não existe
    response = client.post("/auth/login", json={
        "email": "naoexiste@rpg.com",
        "password": "senha123"
    })
    assert response.status_code == 401
