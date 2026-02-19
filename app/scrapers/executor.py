from concurrent.futures import ThreadPoolExecutor
from app.scrapers.generic_crawler import GenericCrawler
from app.core.logger import Logger

def run_scraping(payload):

    logger = Logger()

    crawler = GenericCrawler(payload, logger)

    with ThreadPoolExecutor(max_workers=payload.workers or 4) as executor:

        futures = [
            executor.submit(crawler.crawl_entry, entry)
            for entry in payload.entry_points
        ]

        results = set()

        for f in futures:
            results.update(f.result())

    return {
        "count": len(results),
        "products": list(results)
    }
