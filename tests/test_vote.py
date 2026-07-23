from app.models import Character


def test_vote_character_success(client, db):
    character = Character(swapi_id=1, name="Leia Organa", vote_count=0)
    db.add(character)
    db.commit()
    db.refresh(character)

    response = client.post(f"/characters/{character.id}/vote")
    assert response.status_code == 200
    body = response.json()
    assert "Leia Organa" in body["message"]
    assert "1" in body["message"]

def test_vote_character_not_found(client):
    response = client.post("/characters/123/vote")
    assert response.status_code == 404
    assert "Entity on character with id 123 not found"