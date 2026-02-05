from app.browsers.selenium import SeleniumBrowser
from datetime import datetime

class WorkflowContext:
    def __init__(self, run_id, headless=True, dispatcher=None):
        self.run_id = run_id
        self.browser = SeleniumBrowser(headless=headless)
        self.dispatcher = dispatcher

        self.data = {}
        self.logs = []

    def log(self, message, level = "INFO"):
        entry = {
            "run_id": self.run_id,
            "level": level,
            "timestamp": datetime.utcnow().isoformat(),
            "message": message
        }
        self.logs.append(entry)
        print(f"[{self.run_id}] [{level}] {message}")

    def close(self):
        self.browser.close()