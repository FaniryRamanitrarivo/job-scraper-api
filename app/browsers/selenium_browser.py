import time
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.browsers.base_browser import BaseBrowser
from app.core.selenium_pool import get_selenium_pool


class SeleniumBrowser(BaseBrowser):

    def __init__(
        self,
        headless=True,
        page_timeout=20,
        element_timeout=15,
        retries=2
    ):
        self.page_timeout = page_timeout
        self.element_timeout = element_timeout
        self.retries = retries
        self.headless = headless

        # Acquire driver from pool
        pool = get_selenium_pool()
        self.driver = pool.acquire()
        self.driver.set_page_load_timeout(self.page_timeout)

        logger.info("Selenium browser acquired")

    # -------------------------

    def open(self, url):

        last_exception = None

        for attempt in range(self.retries + 1):

            try:
                logger.info(f"Opening URL: {url}")
                self.driver.get(url)
                return

            except TimeoutException as e:
                logger.warning(f"Timeout loading {url}")
                last_exception = e

            except WebDriverException as e:
                logger.error(f"Driver error: {e}")
                last_exception = e

            if attempt < self.retries:
                logger.info("Retrying open...")
                time.sleep(2)

        raise last_exception

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

    # -------------------------

    def scroll_to_bottom(self):
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error scrolling to bottom: {e}")

    # -------------------------

    def screenshot(self, name="error.png"):
        self.driver.save_screenshot(name)
        logger.info(f"Screenshot saved: {name}")

    # -------------------------

    def quit(self):
        logger.info("Releasing Selenium browser")

        try:
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
            self.driver.get("about:blank")
        except Exception:
            pass

        pool = get_selenium_pool()
        pool.release(self.driver)

