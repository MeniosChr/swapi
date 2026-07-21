import asyncio
import re

import httpx
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Starship, Character, Film
from app.services.swapi_service import fetch_characters, fetch_films, fetch_starships, SwapiError

TIMEOUT = 10.0

def prepare_swapi_resource(item: dict, columns: set[str]) -> dict:
    data = {key: value for key, value in item.items() if key in columns}
    data["swapi_id"] = int(re.search(r"(\d+)/$", item["url"]).group(1))
    if "MGLT" in item:  # starships expose 'MGLT' but the column is 'mglt'
        data["mglt"] = item["MGLT"]
    return data

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
                prepared_entry = prepare_swapi_resource(item, columns)
                if prepared_entry["swapi_id"] in existing_swapi_ids:
                    continue
                db.add(table(**prepared_entry))
                inserted += 1
            counts[table.__tablename__] = inserted

        db.commit()
        print(f"Database populated: {counts}")
    except Exception as e:
        print(f"Database transaction crashed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    return {"inserted": counts}

if __name__ == "__main__":
    asyncio.run(sync_swapi_data())
