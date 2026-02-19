from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.routes.scraping import router as scraping_router
from app.core.selenium_pool import get_selenium_pool

app = FastAPI(title="Job Scraper API")

# Routes
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(scraping_router)

@app.on_event("startup")
def startup():
    get_selenium_pool()._ensure_initialized()