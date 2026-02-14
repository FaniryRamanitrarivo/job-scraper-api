from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app.browser.base import BaseBrowser
import os

class SeleniumBrowser(BaseBrowser):
    def __init__(self, headless=True):
        super().__init__(headless)
        options = Options()
        
        # Configuration pour Docker / Selenium Grid
        if self.headless:
            options.add_argument("--headless=new")
        
        # Ces options sont souvent nécessaires en environnement Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = "eager"

        # On récupère l'URL du hub via une variable d'environnement 
        # (Défaut sur le nom du service docker-compose)
        selenium_url = os.getenv("SELENIUM_URL", "http://selenium_chrome:4444/wd/hub")

        try:
            # On utilise Remote au lieu de Chrome local
            self.driver = webdriver.Remote(
                command_executor=selenium_url,
                options=options
            )
            self.driver.set_page_load_timeout(15)
        except Exception as e:
            print(f"Erreur de connexion au Selenium Grid: {e}")
            raise

    def open(self, url: str):
        self.driver.get(url)

    def find_elements(self, selector: str):
        return self.driver.find_elements("css selector", selector)

    def get_text(self, selector: str) -> str:
        el = self.driver.find_element("css selector", selector)
        return el.text

    def close(self):
        self.driver.quit()
