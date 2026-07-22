from sqlalchemy.orm import sessionmaker


def test_sync_stores_resources(client, engine, monkeypatch):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    monkeypatch.setattr(
        "app.services.sync_services.SessionLocal",
        TestingSessionLocal,
    )

    async def fake_characters(http_client):
        return [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.dev/api/people/1/",
            }
        ]

    async def fake_films(http_client):
        return []

    async def fake_starships(http_client):
        return []

    monkeypatch.setattr(
        "app.services.sync_services.fetch_characters",
        fake_characters,
    )
    monkeypatch.setattr(
        "app.services.sync_services.fetch_films",
        fake_films,
    )
    monkeypatch.setattr(
        "app.services.sync_services.fetch_starships",
        fake_starships,
    )

    response = client.post("/sync")
    assert response.status_code == 200
    body = response.json()
    assert body["inserted"]["character"] == 1
    assert body["inserted"]["film"] == 0
    assert body["inserted"]["starship"] == 0

    listed = client.get("/characters")
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["name"] == "Luke Skywalker"


def test_sync_swapi_error_returns_503(client, monkeypatch):
    from app.services.swapi_service import SwapiError

    async def boom(http_client):
        raise SwapiError("SWAPI is down")

    monkeypatch.setattr("app.services.sync_services.fetch_characters", boom)
    monkeypatch.setattr("app.services.sync_services.fetch_films", boom)
    monkeypatch.setattr("app.services.sync_services.fetch_starships", boom)

    response = client.post("/sync")
    assert response.status_code == 503
