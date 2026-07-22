"""drop unused indexes keep name title swapi unique

Revision ID: 65d88b09815b
Revises: 9f97548ed59d
Create Date: 2026-07-22 18:50:28.983491

"""
from typing import Sequence, Union

from alembic import op


revision: str = "65d88b09815b"
down_revision: Union[str, Sequence[str], None] = "9f97548ed59d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("character", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_character_birth_year"))
        batch_op.drop_index(batch_op.f("ix_character_created"))
        batch_op.drop_index(batch_op.f("ix_character_edited"))
        batch_op.drop_index(batch_op.f("ix_character_eye_color"))
        batch_op.drop_index(batch_op.f("ix_character_gender"))
        batch_op.drop_index(batch_op.f("ix_character_hair_color"))
        batch_op.drop_index(batch_op.f("ix_character_height"))
        batch_op.drop_index(batch_op.f("ix_character_homeworld"))
        batch_op.drop_index(batch_op.f("ix_character_id"))
        batch_op.drop_index(batch_op.f("ix_character_mass"))
        batch_op.drop_index(batch_op.f("ix_character_skin_color"))
        batch_op.drop_index(batch_op.f("ix_character_url"))

    with op.batch_alter_table("film", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_film_created"))
        batch_op.drop_index(batch_op.f("ix_film_director"))
        batch_op.drop_index(batch_op.f("ix_film_edited"))
        batch_op.drop_index(batch_op.f("ix_film_episode_id"))
        batch_op.drop_index(batch_op.f("ix_film_id"))
        batch_op.drop_index(batch_op.f("ix_film_opening_crawl"))
        batch_op.drop_index(batch_op.f("ix_film_producer"))
        batch_op.drop_index(batch_op.f("ix_film_release_date"))
        batch_op.drop_index(batch_op.f("ix_film_url"))

    with op.batch_alter_table("starship", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_starship_cargo_capacity"))
        batch_op.drop_index(batch_op.f("ix_starship_consumables"))
        batch_op.drop_index(batch_op.f("ix_starship_cost_in_credits"))
        batch_op.drop_index(batch_op.f("ix_starship_created"))
        batch_op.drop_index(batch_op.f("ix_starship_crew"))
        batch_op.drop_index(batch_op.f("ix_starship_edited"))
        batch_op.drop_index(batch_op.f("ix_starship_hyperdrive_rating"))
        batch_op.drop_index(batch_op.f("ix_starship_id"))
        batch_op.drop_index(batch_op.f("ix_starship_length"))
        batch_op.drop_index(batch_op.f("ix_starship_manufacturer"))
        batch_op.drop_index(batch_op.f("ix_starship_max_atmosphering_speed"))
        batch_op.drop_index(batch_op.f("ix_starship_mglt"))
        batch_op.drop_index(batch_op.f("ix_starship_model"))
        batch_op.drop_index(batch_op.f("ix_starship_passengers"))
        batch_op.drop_index(batch_op.f("ix_starship_starship_class"))
        batch_op.drop_index(batch_op.f("ix_starship_url"))


def downgrade() -> None:
    with op.batch_alter_table("starship", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_starship_url"), ["url"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_starship_class"), ["starship_class"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_passengers"), ["passengers"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_model"), ["model"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_mglt"), ["mglt"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_starship_max_atmosphering_speed"),
            ["max_atmosphering_speed"],
            unique=False,
        )
        batch_op.create_index(batch_op.f("ix_starship_manufacturer"), ["manufacturer"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_length"), ["length"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_hyperdrive_rating"), ["hyperdrive_rating"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_edited"), ["edited"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_crew"), ["crew"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_created"), ["created"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_cost_in_credits"), ["cost_in_credits"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_consumables"), ["consumables"], unique=False)
        batch_op.create_index(batch_op.f("ix_starship_cargo_capacity"), ["cargo_capacity"], unique=False)

    with op.batch_alter_table("film", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_film_url"), ["url"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_release_date"), ["release_date"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_producer"), ["producer"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_opening_crawl"), ["opening_crawl"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_episode_id"), ["episode_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_edited"), ["edited"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_director"), ["director"], unique=False)
        batch_op.create_index(batch_op.f("ix_film_created"), ["created"], unique=False)

    with op.batch_alter_table("character", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_character_url"), ["url"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_skin_color"), ["skin_color"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_mass"), ["mass"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_homeworld"), ["homeworld"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_height"), ["height"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_hair_color"), ["hair_color"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_gender"), ["gender"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_eye_color"), ["eye_color"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_edited"), ["edited"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_created"), ["created"], unique=False)
        batch_op.create_index(batch_op.f("ix_character_birth_year"), ["birth_year"], unique=False)
