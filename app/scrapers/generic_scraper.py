class GenericScraper:

    def __init__(self, browser, payload, log):
        self.browser = browser
        self.payload = payload
        self.log = log
        self.visited = set()

    # -------------------------

    def open_once(self, url):

        if url in self.visited:
            return False

        self.browser.open(url)
        self.visited.add(url)
        return True

    # -------------------------

    def extract(self, config):

        elements = self.browser.find_elements(config.selector)

        results = []

        for el in elements:

            val = el.get_attribute(config.attribute) if config.attribute else el.text

            if not val:
                continue

            if config.regex:
                import re
                m = re.search(config.regex, val)
                if not m:
                    continue
                val = m.group(0)

            results.append(val)

        return results

    # -------------------------

    def paginate(self, base_url):

        yield base_url

        if not self.payload.pagination:
            return

        if self.payload.pagination.type == "parameter_increment":

            for i in range(2, self.payload.pagination.max_pages + 1):

                yield base_url + self.payload.pagination.parameter.replace(
                    "<PNum>", str(i)
                )

    # -------------------------

    def scrape_entry(self, entry):

        pages = [entry]

        # navigation
        if self.payload.navigation:

            for step in self.payload.navigation:

                new_pages = []

                for page in pages:

                    self.open_once(page)

                    new_pages.extend(self.extract(step.extract))

                pages = new_pages

        # listing
        products = set()

        for page in pages:

            for url in self.paginate(page):

                self.open_once(url)

                products.update(
                    self.extract(self.payload.product_links)
                )

        return products
