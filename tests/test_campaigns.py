def test_admin_cria_campanha(client, admin_token):
    #admin deve conseguir criar campanha
    response = client.post("/campaigns/", json={
        "title": "A Maldição do Dragão",
        "description": "Uma aventura épica",
        "setting": "Alta Fantasia",
        "max_players": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "A Maldição do Dragão"
    assert data["status"] == "recruiting"


def test_player_nao_pode_criar_campanha(client, player_token):
    #player não deve conseguir criar campanha
    response = client.post("/campaigns/", json={
        "title": "Campanha do Player",
        "max_players": 4
    }, headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 403


def test_listar_campanhas(client, admin_token):
    #qualquer usuário autenticado pode listar campanhas
    client.post("/campaigns/", json={
        "title": "Campanha 1",
        "max_players": 4
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/campaigns/",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_buscar_campanha_por_id(client, admin_token):
    #testa buscar uma campanha específica
    client.post("/campaigns/", json={
        "title": "Campanha Teste",
        "max_players": 4
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/campaigns/1",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Campanha Teste"


def test_buscar_campanha_inexistente(client, admin_token):
    #deve retornar 404 para campanha que não existe
    response = client.get("/campaigns/999",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404


def test_admin_atualiza_campanha(client, admin_token):
    #admin pode atualizar sua própria campanha
    client.post("/campaigns/", json={
        "title": "Campanha Antiga",
        "max_players": 4
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.put("/campaigns/1", json={
        "title": "Campanha Nova",
        "status": "ongoing"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Campanha Nova"
    assert response.json()["status"] == "ongoing"


def test_admin_deleta_campanha(client, admin_token):
    #admin pode deletar sua própria campanha
    client.post("/campaigns/", json={
        "title": "Campanha para deletar",
        "max_players": 4
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.delete("/campaigns/1",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
