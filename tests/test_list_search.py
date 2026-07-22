from app.models import Character, Film

def test_list_characters_empty(client):
    response = client.get("/characters")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []
    assert body["page"] == 1

def test_search_characters_by_name(client, db):
    db.add(
        Character(
            swapi_id=1,
            name="Luke Skywalker",
            vote_count=0,
        )
    )
    db.commit()
    response = client.get("/characters/search", params={"name": "luke"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["name"] == "Luke Skywalker"

def test_search_characters_by_name_not_found(client, db):
    response = client.get("/characters/search", params={"name": "luke"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_list_films_and_search_by_title(client, db):
    db.add(
        Film(
            swapi_id=1,
            title="A New Hope",
            vote_count=0,
        )
    )
    db.commit()
    listed = client.get("/films")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["title"] == "A New Hope"
    search = client.get("/films/search", params={"name": "hope"})
    assert search.status_code == 200
    assert search.json()["total"] == 1
    assert search.json()["items"][0]["title"] == "A New Hope"