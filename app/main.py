from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.runs import router as runs_router


app = FastAPI(title="Job Scraper API")
app.include_router(health_router)
app.include_router(runs_router)