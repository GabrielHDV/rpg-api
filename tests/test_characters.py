def test_player_cria_personagem(client, admin_token, player_token):
    #cria uma campanha primeiro
    client.post("/campaigns/", json={
        "title": "Campanha Teste",
        "max_players": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})

    #player cria personagem na campanha
    response = client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 1,
        "campaign_id": 1
    }, headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Frodo"
    assert data["campaign_id"] == 1


def test_level_invalido(client, player_token):
    #nível fora do intervalo 1-20 deve ser rejeitado
    response = client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 25
    }, headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 422


def test_campanha_cheia(client, admin_token, player_token):
    #não deve aceitar personagem em campanha cheia
    client.post("/campaigns/", json={
        "title": "Campanha Pequena",
        "max_players": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})

    #primeiro personagem entra normalmente
    client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 1,
        "campaign_id": 1
    }, headers={"Authorization": f"Bearer {player_token}"})

    #segundo personagem deve ser bloqueado
    response = client.post("/characters/", json={
        "name": "Sam",
        "race": "Hobbit",
        "char_class": "Guerreiro",
        "level": 1,
        "campaign_id": 1
    }, headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 400


def test_listar_meus_personagens(client, player_token):
    #player só vê seus próprios personagens
    client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 1
    }, headers={"Authorization": f"Bearer {player_token}"})
    response = client.get("/characters/",
        headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_player_nao_ve_personagens_de_outros(client, admin_token, player_token):
    #player não pode acessar personagens de outros
    client.post("/characters/", json={
        "name": "Gandalf",
        "race": "Mago",
        "char_class": "Feiticeiro",
        "level": 20
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/characters/1",
        headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 403


def test_player_atualiza_personagem(client, player_token):
    #player pode atualizar seu próprio personagem
    client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 1
    }, headers={"Authorization": f"Bearer {player_token}"})
    response = client.put("/characters/1", json={
        "level": 5
    }, headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 200
    assert response.json()["level"] == 5


def test_player_deleta_personagem(client, player_token):
    #player pode deletar seu próprio personagem
    client.post("/characters/", json={
        "name": "Frodo",
        "race": "Hobbit",
        "char_class": "Ladino",
        "level": 1
    }, headers={"Authorization": f"Bearer {player_token}"})
    response = client.delete("/characters/1",
        headers={"Authorization": f"Bearer {player_token}"})
    assert response.status_code == 204
