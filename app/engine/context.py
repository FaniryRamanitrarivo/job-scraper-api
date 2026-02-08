from typing import Any, Dict, Optional

class WorkflowContext:
    def __init__(self, run_id: str, browser):
        self.run_id = run_id
        self.browser = browser
        self.data = {}
        self.logs = []

        self.current_item: Optional[Any] = None
        self.current_object: Optional[Dict[str, Any]] = None

    def log(self, message: str, level: str = "INFO"):
        full_msg = f"[{self.run_id}] [{level}] {message}"
        self.logs.append(full_msg)
        print(full_msg)


    def close(self):
        if self.browser:
            self.browser.close()
