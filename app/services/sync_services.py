import asyncio
import re
import httpx

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Starship, Character, Film
from app.services.swapi_service import fetch_characters, fetch_films, fetch_starships, SwapiError, TIMEOUT

class EntityNotFoundError(Exception):
    """Raised when a local DB entity is missing (maps to HTTP 404)."""
    pass

def _get_swapi_id(url: str) -> int:
    return int(re.search(r"(\d+)/$", url).group(1))

def _prepare_swapi_resource(item: dict, columns: set[str]) -> dict:
    data = {key: value for key, value in item.items() if key in columns}
    data["swapi_id"] = _get_swapi_id(item["url"])
    if "MGLT" in item:  # starships expose 'MGLT' but the column is 'mglt'
        data["mglt"] = item["MGLT"]
    return data

def _append_unique_from_urls(related_items, urls: list, lookup_by_swapi_id: dict):
    for url in urls:
        related = lookup_by_swapi_id.get(_get_swapi_id(url))
        if related is not None and related not in related_items:
            related_items.append(related)

def _link_character_relations(
    characters: list[dict],
    characters_by_swapi_id: dict,
    films_by_swapi_id: dict,
    starships_by_swapi_id: dict,
) -> None:
    for item in characters:
        character = characters_by_swapi_id.get(_get_swapi_id(item["url"]))
        if character is None:
            continue
        _append_unique_from_urls(character.films, item.get("films", []), films_by_swapi_id)
        _append_unique_from_urls(character.starships, item.get("starships", []), starships_by_swapi_id)

def _link_film_relations(
    films: list[dict],
    films_by_swapi_id: dict,
    starships_by_swapi_id: dict,
) -> None:
    for item in films:
        film = films_by_swapi_id.get(_get_swapi_id(item["url"]))
        if film is None:
            continue
        _append_unique_from_urls(film.starships, item.get("starships", []), starships_by_swapi_id)

async def sync_swapi_data():
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            starships = await fetch_starships(client)
            films = await fetch_films(client)
            characters = await fetch_characters(client)
        except SwapiError:
            raise
        except Exception as e:
            raise SwapiError(f"Unexpected error: {e}")

    print("Starting database population...")

    data_by_table = {
        Film: films,
        Starship: starships,
        Character: characters,
    }

    db = SessionLocal()
    try:
        counts = {}
        for table, items in data_by_table.items():
            columns = {column.name for column in table.__table__.columns}
            existing_swapi_ids = set(db.scalars(select(table.swapi_id)))
            inserted = 0
            for item in items:
                prepared_entry = _prepare_swapi_resource(item, columns)
                if prepared_entry["swapi_id"] in existing_swapi_ids:
                    continue
                db.add(table(**prepared_entry))
                inserted += 1
            counts[table.__tablename__] = inserted
        db.flush()

        characters_by_swapi_id = {c.swapi_id: c for c in db.scalars(select(Character))}
        films_by_swapi_id      = {f.swapi_id: f for f in db.scalars(select(Film))}
        starships_by_swapi_id  = {s.swapi_id: s for s in db.scalars(select(Starship))}

        _link_character_relations(
            characters,
            characters_by_swapi_id,
            films_by_swapi_id,
            starships_by_swapi_id,
        )
        _link_film_relations(films, films_by_swapi_id, starships_by_swapi_id)

        db.commit()
        print(f"Database populated: {counts}")
    except Exception as e:
        print(f"Database transaction crashed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    return {"inserted": counts}

def get_paginated(db: Session, model, page: int, page_size: int):
    offset = (page - 1) * page_size
    entries = db.scalars(
        select(model).order_by(model.id).offset(offset).limit(page_size)
    ).all()
    total = db.scalar(select(func.count()).select_from(model))
    return entries, total

def search_paginated(db: Session, model, column, term: str, page: int, page_size: int):
    offset = (page - 1) * page_size
    filter_expr = column.ilike(f"%{term}%")
    entries = db.scalars(
        select(model).where(filter_expr).order_by(model.id).offset(offset).limit(page_size)
    ).all()
    total = db.scalar(select(func.count()).select_from(model).where(filter_expr))
    return entries, total

def vote_entity(db: Session, model, entity_id: int):
    entity = db.get(model, entity_id)
    if entity is None:
        raise EntityNotFoundError(
            f"Entity on {model.__tablename__} with id {entity_id} not found"
        )

    entity.vote_count += 1
    db.commit()

    # Films use title, characters & starships use name
    label = getattr(entity, "name", None) or entity.title
    return entity.vote_count, label

if __name__ == "__main__":
    asyncio.run(sync_swapi_data())
