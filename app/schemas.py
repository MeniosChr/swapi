from pydantic import BaseModel, ConfigDict

class CharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    swapi_id: int
    height: str | None = None
    mass: str | None = None
    hair_color: str | None = None
    skin_color: str | None = None
    eye_color: str | None = None
    birth_year: str | None = None
    gender: str | None = None
    homeworld: str | None = None
    # films: list[FilmResponse] = []
    species: list[str] = []
    vehicles: list[str] = []
    # starships: list[StarshipResponse] = []
    created: str | None = None
    edited: str | None = None
    url: str | None = None

class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    swapi_id: int
    episode_id: int | None = None
    opening_crawl: str | None = None
    director: str | None = None
    producer: str | None = None
    release_date: str | None = None
    # characters: list[CharacterResponse] = []
    planets: list[str] = []
    # starships: list[StarshipResponse] = []
    vehicles: list[str] = []
    species: list[str] = []
    created: str | None = None
    edited: str | None = None
    url: str | None = None

class StarshipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    swapi_id: int
    model: str | None = None
    manufacturer: str | None = None
    cost_in_credits: str | None = None
    length: str | None = None
    max_atmosphering_speed: str | None = None
    crew: str | None = None
    passengers: str | None = None
    cargo_capacity: str | None = None
    consumables: str | None = None
    hyperdrive_rating: str | None = None
    mglt: str | None = None
    starship_class: str | None = None
    pilots: list[str] = []
    # films: list[str] = []
    created: str | None = None
    edited: str | None = None
    url: str | None = None


class CharacterPage(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[CharacterResponse]

class FilmPage(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[FilmResponse]

class StarshipPage(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[StarshipResponse]