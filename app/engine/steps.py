from app.browsers.selenium import SeleniumBrowser

def fetch_urls(step, run_id):
    url = step.get("url")
    selector = step.get("selector")

    browser = SeleniumBrowser(headless=True)

    browser.open(url)

    elements = browser.find_elements(selector)

    urls = [el.get_attribute("href") for el in elements if el.get_attribute("href")]


    browser.close()
    print(f"[{run_id}] Fetched urls: {urls}")

    return urls


def fetch_details(step, run_id):
    url = step.get("url")
    fields = step.get("fields", {})

    browser = SeleniumBrowser(headless=True)
    browser.open(url)

    details = {}

    for key, selector in fields.items():
        elements = browser.find_elements(selector)
        details[key] = browser.get_text(elements[0]) if elements else ""

    browser.close()
    print(f"[{run_id}] Fetched details: {details}")

    return details