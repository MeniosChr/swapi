from sqlalchemy import Integer, Column, Table, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


character_films = Table("character_films", Base.metadata,
    Column("character_id", ForeignKey("character.id"), primary_key=True),
    Column("film_id", ForeignKey("film.id"), primary_key=True)
)

character_starships = Table("character_starships", Base.metadata,
    Column("character_id", ForeignKey("character.id"), primary_key=True),
    Column("starship_id", ForeignKey("starship.id"), primary_key=True)
)

film_starships = Table("film_starships", Base.metadata,
    Column("film_id", ForeignKey("film.id"), primary_key=True),
    Column("starship_id", ForeignKey("starship.id"), primary_key=True)
)

class Character(Base):
    __tablename__ = "character"
    id         : Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    swapi_id   : Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    name       : Mapped[str] = mapped_column(String, index=True, nullable=False)
    height     : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    mass       : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    hair_color : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    skin_color : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    eye_color  : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    birth_year : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    gender     : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    homeworld  : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    films      : Mapped[list["Film"]] = relationship("Film", secondary = character_films, back_populates="characters")
    species    : Mapped[list | None] = mapped_column(JSON, nullable=True)
    vehicles   : Mapped[list | None] = mapped_column(JSON, nullable=True)
    starships  : Mapped[list["Starship"]] = relationship("Starship", secondary = character_starships, back_populates="characters")
    created    : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    edited     : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    url        : Mapped[str | None] = mapped_column(String, index=True, nullable=True)

class Film(Base):
    __tablename__ = "film"
    id            : Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    swapi_id      : Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    title         : Mapped[str] = mapped_column(String, index=True, nullable=False)
    episode_id    : Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    opening_crawl : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    director      : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    producer      : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    release_date  : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    characters    : Mapped[list["Character"]] = relationship("Character", secondary = character_films, back_populates="films")
    planets       : Mapped[list | None] = mapped_column(JSON, nullable=True)
    starships     : Mapped[list["Starship"]] = relationship("Starship", secondary = film_starships, back_populates="films")
    vehicles      : Mapped[list | None] = mapped_column(JSON, nullable=True)
    species       : Mapped[list | None] = mapped_column(JSON, nullable=True)
    created       : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    edited        : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    url           : Mapped[str | None] = mapped_column(String, index=True, nullable=True)

class Starship(Base):
    __tablename__ = "starship"
    id                     : Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    swapi_id               : Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    name                   : Mapped[str] = mapped_column(String, index=True, nullable=False)
    model                  : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    manufacturer           : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    cost_in_credits        : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    length                 : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    max_atmosphering_speed : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    crew                   : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    passengers             : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    cargo_capacity         : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    consumables            : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    hyperdrive_rating      : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    mglt                   : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    starship_class         : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    pilots                 : Mapped[list | None] = mapped_column(JSON, nullable=True)
    characters             : Mapped[list["Character"]] = relationship("Character", secondary = character_starships, back_populates="starships")
    films                  : Mapped[list["Film"]] = relationship("Film", secondary = film_starships, back_populates="starships")
    created                : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    edited                 : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    url                    : Mapped[str | None] = mapped_column(String, index=True, nullable=True)