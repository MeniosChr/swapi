from pydantic import BaseModel, ConfigDict, Field

class CharacterSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    swapi_id: int


class FilmSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    swapi_id: int


class StarshipSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    swapi_id: int

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
    films: list[FilmSummary] = Field(default_factory=list)
    species: list[str] | None = None
    vehicles: list[str] | None = None
    starships: list[StarshipSummary] = Field(default_factory=list)
    created: str | None = None
    edited: str | None = None
    url: str | None = None
    vote_count: int = 0

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
    characters: list[CharacterSummary] = Field(default_factory=list)
    planets: list[str] | None = None
    starships: list[StarshipSummary] = Field(default_factory=list)
    vehicles: list[str] | None = None
    species: list[str] | None = None
    created: str | None = None
    edited: str | None = None
    url: str | None = None
    vote_count: int = 0

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
    pilots: list[str] | None = None
    characters: list[CharacterSummary] = Field(default_factory=list)
    films: list[FilmSummary] = Field(default_factory=list)
    created: str | None = None
    edited: str | None = None
    url: str | None = None
    vote_count: int = 0

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
