from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class SeleniumBrowser:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def open(self, url):
        self.driver.get(url)
        time.sleep(1)  # attend que la page charge

    def find_elements(self, selector, by="css"):
        if by == "css":
            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        elif by == "xpath":
            return self.driver.find_elements(By.XPATH, selector)
        else:
            raise ValueError("by doit être 'css' ou 'xpath'")

    def get_text(self, element):
        return element.text

    def close(self):
        self.driver.quit()
