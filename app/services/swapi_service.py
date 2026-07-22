import httpx

BASE_URL = "https://swapi.dev/api"
TIMEOUT = 10.0

class SwapiError(Exception):
    """Raised when SWAPI cannot provide a complete, valid response."""
    pass

async def fetch_resources(client: httpx.AsyncClient, resource_url: str) -> list[dict]:
    results = []
    url = f"{BASE_URL}/{resource_url}/"

    while url:
        try:
            response = await client.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SwapiError(f"Failed to fetch '{resource_url}' from SWAPI") from exc

        results.extend(data.get("results", []))
        url = data.get("next")

    return results


async def fetch_characters(client: httpx.AsyncClient) -> list[dict]:
    return await fetch_resources(client, "people")

async def fetch_films(client: httpx.AsyncClient) -> list[dict]:
    return await fetch_resources(client, "films")

async def fetch_starships(client: httpx.AsyncClient) -> list[dict]:
    return await fetch_resources(client, "starships")