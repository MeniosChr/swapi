from fastapi import FastAPI, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Character, Film, Starship
from app.schemas import CharacterPage, FilmPage, StarshipPage
from app.services.sync_services import sync_swapi_data, get_paginated, search_paginated, vote_entity
from app.services.swapi_service import SwapiError

app = FastAPI(title="Star Wars API")

@app.get("/health")
def health_check():
    return "up"

@app.get("/")
def status():
    return {"status": "ok"}

@app.post("/sync")
async def sync():
    try:
        return await sync_swapi_data()
    except SwapiError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

@app.get("/characters", response_model=CharacterPage)
def list_characters(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    characters, total = get_paginated(db, Character, page, page_size)
    return CharacterPage(
        page=page,
        page_size=page_size,
        total=total,
        items=characters,
    )

@app.get("/characters/search", response_model=CharacterPage)
def search_characters(
        db: Session = Depends(get_db),
        name: str = Query(..., min_length=1),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    characters, total = search_paginated(db, Character, Character.name, name, page, page_size)
    return CharacterPage(
        page=page,
        page_size=page_size,
        total=total,
        items=characters,
    )

@app.post("/characters/{character_id}/vote")
def vote_character(
        db: Session = Depends(get_db),
        character_id: int = Path(..., ge=1),
    ):
    try:
        voted_entity_count, voted_entity_name = vote_entity(db, Character, character_id)
    except SwapiError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "message": f"Character with name `{voted_entity_name}` voted successfully. Total votes: {voted_entity_count}"
    }

@app.get("/films", response_model=FilmPage)
def list_films(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    films, total = get_paginated(db, Film, page, page_size)
    return FilmPage(
        page=page,
        page_size=page_size,
        total=total,
        items=films,
    )

@app.get("/films/search", response_model=FilmPage)
def search_films(
        db: Session = Depends(get_db),
        name: str = Query(..., min_length=1),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    films, total = search_paginated(db, Film, Film.title, name, page, page_size)
    return FilmPage(
        page=page,
        page_size=page_size,
        total=total,
        items=films,
    )

@app.post("/films/{film_id}/vote")
def vote_film(
        db: Session = Depends(get_db),
        film_id: int = Path(..., ge=1),
    ):
    try:
        voted_entity_count, voted_entity_name = vote_entity(db, Film, film_id)
    except SwapiError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "message": f"Film with title `{voted_entity_name}` voted successfully. Total votes: {voted_entity_count}"
    }

@app.get("/starships", response_model=StarshipPage)
def list_starships(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    starships, total = get_paginated(db, Starship, page, page_size)
    return StarshipPage(
        page=page,
        page_size=page_size,
        total=total,
        items=starships,
    )

@app.get("/starships/search", response_model=StarshipPage)
def search_starships(
        db: Session = Depends(get_db),
        name: str = Query(..., min_length=1),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
    ):
    starships, total = search_paginated(db, Starship, Starship.name, name, page, page_size)
    return StarshipPage(
        page=page,
        page_size=page_size,
        total=total,
        items=starships,
    )

@app.post("/starships/{starship_id}/vote")
def vote_starship(
        db: Session = Depends(get_db),
        starship_id: int = Path(..., ge=1),
    ):
    try:
        vote_count, label = vote_entity(db, Starship, starship_id)
    except SwapiError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "message": f"Starship with name `{label}` voted successfully. Total votes: {vote_count}"
    }