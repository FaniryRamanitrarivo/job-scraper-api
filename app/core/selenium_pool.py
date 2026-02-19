# app/core/selenium_pool.py

from queue import Queue, Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from loguru import logger
import threading
import os

class SeleniumPool:
    def __init__(self, size=3, grid_url="http://selenium_chrome:4444/wd/hub"):
        self.pool = Queue(maxsize=size)
        self.grid_url = grid_url
        self.lock = threading.Lock()
        self.size = size
        self.initialized = False

    def _create_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Remote(
            command_executor=self.grid_url,
            options=chrome_options
        )

        logger.info("Selenium driver created")
        return driver

    def _ensure_initialized(self):
        if self.initialized:
            return

        with self.lock:
            if self.initialized:
                return

            logger.info("Initializing Selenium pool...")

            for _ in range(self.size):
                driver = self._create_driver()
                self.pool.put(driver)

            self.initialized = True
            logger.success("Selenium pool ready")

    def acquire(self, timeout=30):
        self._ensure_initialized()

        try:
            driver = self.pool.get(timeout=timeout)
            logger.info("Selenium driver acquired")
            return driver
        except Empty:
            raise RuntimeError("No Selenium driver available")

    def release(self, driver):
        try:
            driver.title  # test vivant
            self.pool.put(driver)
        except:
            logger.warning("Driver dead, recreating")
            self.pool.put(self._create_driver())

    def shutdown(self):
        logger.info("Shutting down Selenium pool...")
        while not self.pool.empty():
            driver = self.pool.get_nowait()
            try:
                driver.quit()
            except Exception:
                pass
        logger.info("Selenium pool shutdown complete")


# ✅ Lazy singleton
_selenium_pool_instance = None

def get_selenium_pool():
    global _selenium_pool_instance
    if _selenium_pool_instance is None:
        url = os.getenv("SELENIUM_URL", "http://selenium_chrome:4444/wd/hub")
        _selenium_pool_instance = SeleniumPool(size=2, grid_url=url)
    return _selenium_pool_instance
