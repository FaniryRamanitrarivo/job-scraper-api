from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from loguru import logger
from app.browsers.base_browser import BaseBrowser
import time
import os

class SeleniumBrowser(BaseBrowser):

    def __init__(
        self,
        headless=True,
        page_timeout=30,
        element_timeout=15,
        retries=2
    ):
        self.page_timeout = page_timeout
        self.element_timeout = element_timeout
        self.retries = retries

        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-allow-origins=*")


        selenium_url = os.getenv(
            "SELENIUM_URL",
            "http://selenium_chrome:4444/wd/hub"
        )

        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Remote(
            command_executor=selenium_url,
            options=chrome_options
        )
        self.driver.set_page_load_timeout(self.page_timeout)

        logger.info("Selenium browser started")

    # -------------------------

    def open(self, url):

        for attempt in range(self.retries + 1):

            try:
                logger.info(f"Opening URL: {url}")
                self.driver.get(url)
                return

            except TimeoutException:
                logger.warning(f"Timeout loading {url}")

            except WebDriverException as e:
                logger.error(f"Driver error: {e}")

            if attempt < self.retries:
                logger.info("Retrying open...")
                time.sleep(2)
            else:
                raise

    # -------------------------

    def find_elements(self, selector, by=By.CSS_SELECTOR):

        try:
            WebDriverWait(self.driver, self.element_timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException:
            logger.warning(f"No elements found for selector: {selector}")
            return []

        elements = self.driver.find_elements(by, selector)

        logger.info(f"{len(elements)} elements found for {selector}")

        return elements

    # -------------------------

    def wait_for(self, selector, by=By.CSS_SELECTOR):

        WebDriverWait(self.driver, self.element_timeout).until(
            EC.presence_of_element_located((by, selector))
        )

    # -------------------------

# -------------------------
    def get_text(self, element):
        try:
            return element.text
        except Exception as e:
            logger.error(f"Error getting text: {e}")
            return ""

    def get_attribute(self, element, attr: str):
        try:
            return element.get_attribute(attr)
        except Exception as e:
            logger.error(f"Error getting attribute '{attr}': {e}")
            return None

    def scroll_to_bottom(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # petite pause pour laisser le scroll se stabiliser
        except Exception as e:
            logger.error(f"Error scrolling to bottom: {e}")

    def screenshot(self, name="error.png"):
        self.driver.save_screenshot(name)
        logger.info(f"Screenshot saved: {name}")

    # -------------------------

    def quit(self):
        logger.info("Closing Selenium browser")
        self.driver.quit()
