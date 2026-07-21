from fastapi import FastAPI, HTTPException
from app.services.sync_services import sync_swapi_data
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