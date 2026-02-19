from app.core.browser_pool import browser_pool
from app.core.http_client import http_client
from app.core.crawler_queue import CrawlerQueue
from app.scrapers.extractor import Extractor

class GenericCrawler:

    def __init__(self, payload, logger):

        self.payload = payload
        self.log = logger
        self.products = set()

    # -------------------------

    def _fetch(self, url, engine):

        if engine == "requests":
            return http_client.get(url)

        browser = browser_pool.acquire()

        try:
            browser.open(url)
            return browser.page_source()
        finally:
            browser_pool.release(browser)

    # -------------------------

    def _detect_engine(self):

        if self.payload.engine == "requests":
            return "requests"

        if self.payload.engine == "selenium":
            return "selenium"

        # AUTO
        if self.payload.requires_js:
            return "selenium"

        return "requests"

    # -------------------------

    def crawl_entry(self, entry):

        queue = CrawlerQueue()
        queue.push(entry)

        engine = self._detect_engine()

        while not queue.empty():

            url = queue.pop()

            try:
                html_text = self._fetch(url, engine)

            except Exception as e:
                self.log.error("CRAWLER", f"Fetch failed {url}: {e}")
                continue

            # navigation steps
            if self.payload.navigation:

                for step in self.payload.navigation:

                    new_pages = Extractor.extract(html_text, step.extract)

                    for p in new_pages:
                        queue.push(p)

                continue

            # product links
            links = Extractor.extract(
                html_text,
                self.payload.product_links
            )

            self.products.update(links)

            # pagination
            if self.payload.pagination \
               and self.payload.pagination.type == "parameter_increment":

                for i in range(2, self.payload.pagination.max_pages + 1):

                    next_url = url + self.payload.pagination.parameter.replace(
                        "<PNum>", str(i)
                    )

                    queue.push(next_url)

        return self.products
