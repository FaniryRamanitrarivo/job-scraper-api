import re
from lxml import html

class Extractor:

    @staticmethod
    def extract(html_text, config):

        tree = html.fromstring(html_text)

        values = tree.xpath(config.selector)

        results = []

        for v in values:

            if hasattr(v, "text_content"):
                v = v.text_content()

            if isinstance(v, str) is False:
                v = str(v)

            if config.regex:
                m = re.search(config.regex, v)
                if not m:
                    continue
                v = m.group(0)

            results.append(v.strip())

        return results
