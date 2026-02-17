from fastapi import APIRouter
from app.models.scraping_payload import ScrapingPayload
from app.scrapers.executor import run_scraping
from loguru import logger

router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/")
def scrape(payload: ScrapingPayload):

    return run_scraping(payload)
