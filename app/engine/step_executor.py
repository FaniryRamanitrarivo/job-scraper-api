from typing import Dict, Callable
from app.engine.context import WorkflowContext

class StepExecutor:
    def __init__(self, handlers: Dict[str, Callable]):
        self.handlers = handlers

    def execute(self, step: dict, ctx: WorkflowContext):
        step_type = step.get("type")
        if step_type not in self.handlers:
            raise ValueError(f"Unknown step type: {step_type}")

        ctx.log(f"Executing step: {step_type}")
        self.handlers[step_type](step, ctx)
