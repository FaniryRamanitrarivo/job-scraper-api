from datetime import datetime
from typing import Callable, Optional
from loguru import logger
import uuid

class Logger:

    def __init__(
        self, 
        job_id: Optional[str] = None,
        emitter: Optional[Callable[[dict], None]] = None
    ):
        self.job_id = job_id or str(uuid.uuid4())
        self.emitter = emitter

    def _log(self, level: str, component: str, message: str, **data):

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "job_id": self.job_id,
            "component": component,
            "message": message,
            "data": data
        }

        # console/file log
        getattr(logger, level.lower())(
            f"[{component}] {message}"
        )

        # websocket futur
        if self.emitter:
            self.emitter(event)

    # helpers

    def info(self, component, message, **data):
        self._log("info", component, message, **data)

    def success(self, component, message, **data):
        self._log("success", component, message, **data)

    def warning(self, component, message, **data):
        self._log("warning", component, message, **data)

    def error(self, component, message, **data):
        self._log("error", component, message, **data)