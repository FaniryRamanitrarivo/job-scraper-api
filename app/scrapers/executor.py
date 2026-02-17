from app.browsers.selenium_browser import SeleniumBrowser
from app.models.scraping_payload import ScrapingPayload
from app.scrapers.generic_scraper import GenericScraper
from app.core.logger import Logger

def run_scraping(payload: ScrapingPayload):

    browser = SeleniumBrowser(headless=True)
    logger = Logger()

    try:
        scraper = GenericScraper(browser, payload, logger)
        results = scraper.scrape()
        return {"count": len(results), "products": results}

    finally:
        browser.quit()
