import re
from loguru import logger


class GenericScraper:

    def __init__(self, browser, payload, log):
        self.browser = browser
        self.payload = payload
        self.products = set()
        self.log = log

    def _extract(self, config):

        elements = self.browser.find_elements(config.selector)

        results = []

        for el in elements:

            val = (
                el.get_attribute(config.attribute)
                if config.attribute else el.text
            )

            if not val:
                continue

            if config.regex:
                m = re.search(config.regex, val)
                if not m:
                    continue
                val = m.group(0)

            results.append(val)

        self.log.info(
            "SCRAPER",
            f"Extracted {len(results)} values"
        )
        
        return results

    # -------------------------

    def scrape(self):

        self.log.info(
            "SCRAPER",
            "Starting scraping"
        )

        for entry in self.payload.entry_points:

            self.browser.open(entry)

            pages = [entry]

            # navigation
            if self.payload.navigation:

                for step in self.payload.navigation:

                    self.log.info(
                        "SCRAPER",
                        f"Navigation step: {step.name}"
                    )

                    new_pages = []

                    for page in pages:
                        self.browser.open(page)
                        new_pages.extend(self._extract(step.extract))

                    pages = new_pages

            # listing pages
            for page in pages:

                self.browser.open(page)

                self.products.update(
                    self._extract(self.payload.product_links)
                )

                # pagination parameter_increment
                if self.payload.pagination \
                   and self.payload.pagination.type == "parameter_increment":

                    for i in range(2, self.payload.pagination.max_pages + 1):

                        url = page + self.payload.pagination.parameter.replace(
                            "<PNum>", str(i)
                        )

                        self.browser.open(url)

                        self.products.update(
                            self._extract(self.payload.product_links)
                        )

        self.log.info(
            "SCRAPER",
            f"Scraping finished: {len(self.products)} products"
        )

        return list(self.products)
