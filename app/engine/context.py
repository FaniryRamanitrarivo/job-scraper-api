from app.browser.base import BaseBrowser
from datetime import datetime

class WorkflowContext:
    def __init__(self, run_id: str, browser: BaseBrowser):
        self.run_id = run_id
        self.browser = browser
        self.data = {}
        self.logs = []

    def log(self, message: str, level="INFO"):
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
