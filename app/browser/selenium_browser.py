from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app.browser.base import BaseBrowser

class SeleniumBrowser(BaseBrowser):
    def __init__(self, headless=True):
        super().__init__(headless)
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

    def open(self, url: str):
        self.driver.get(url)

    def find_elements(self, selector: str):
        return self.driver.find_elements("css selector", selector)

    def get_text(self, selector: str) -> str:
        el = self.driver.find_element("css selector", selector)
        return el.text

    def close(self):
        self.driver.quit()
