from queue import Queue
from app.browsers.selenium_browser import SeleniumBrowser


class BrowserPool:

    def __init__(self, size=3):

        self.pool = Queue()

        for _ in range(size):
            self.pool.put(SeleniumBrowser())

    def acquire(self):
        return self.pool.get()

    def release(self, browser):
        self.pool.put(browser)


browser_pool = BrowserPool(size=3)
