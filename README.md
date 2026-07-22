# Star Wars API (SWAPI Backend)

RESTful API built with **FastAPI** that fetches Star Wars data from [SWAPI](https://swapi.dev/), stores it in **SQLite**, and exposes endpoints to list, search, and vote for characters, films, and starships.

Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`

## Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy 2.x + Alembic
- SQLite
- httpx (async SWAPI client)
- pytest + pytest-cov

## Setup

From the project root:

```bash
python -m venv .venv
```

Activate the virtual environment:

- **Git Bash / Linux / macOS:** `source .venv/Scripts/activate` (Windows Git Bash) or `source .venv/bin/activate` (Unix)
- **Windows CMD:** `.venv\Scripts\activate.bat`
- **PowerShell:** `.venv\Scripts\Activate.ps1`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database migrations

Apply the schema (creates/updates `swapi.db`):

```bash
python -m alembic upgrade head
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Server: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Sync data from SWAPI

Fetch characters, films, and starships, store them locally, and build many-to-many relationships.

**Via API:**

```bash
curl -X POST http://127.0.0.1:8000/sync
```

**Via script:**

```bash
python -m app.services.sync_services
```

Sync is idempotent: re-running skips existing `swapi_id` rows and only adds missing relationship links.

## Main endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/sync` | Fetch & store SWAPI data |
| `GET` | `/characters` | Paginated list (`page`, `page_size`) |
| `GET` | `/characters/search?name=` | Search characters by name |
| `POST` | `/characters/{id}/vote` | Vote for a character |
| `GET` | `/films` | Paginated list |
| `GET` | `/films/search?name=` | Search films by title |
| `POST` | `/films/{id}/vote` | Vote for a film |
| `GET` | `/starships` | Paginated list |
| `GET` | `/starships/search?name=` | Search starships by name |
| `POST` | `/starships/{id}/vote` | Vote for a starship |

Pagination query params:

- `page` ≥ 1 (default `1`)
- `page_size` between 1 and 100 (default `10`)

Example:

```bash
curl "http://127.0.0.1:8000/characters?page=1&page_size=5"
curl "http://127.0.0.1:8000/characters/search?name=Luke"
curl -X POST "http://127.0.0.1:8000/characters/1/vote"
```

## Tests

```bash
python -m pytest tests/ -v
```

With coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

External SWAPI calls are mocked in sync tests. Aim: **≥ 80%** coverage (currently above that).

## Project layout

```text
app/
  main.py              # FastAPI routes
  db.py                # Engine, session, get_db
  models.py            # SQLAlchemy models + association tables
  schemas.py           # Pydantic response schemas
  services/
    swapi_service.py   # HTTP client for SWAPI
    sync_services.py   # Sync, pagination, search, vote
alembic/               # Migrations
tests/                 # pytest suite
```

## Notes

- SQLite file `swapi.db` is created locally and is gitignored.
- Stop the API server before deleting `swapi.db` on Windows (file lock).
- Full OpenAPI schema and “Try it out” UI: `/docs` (also `/redoc`).
