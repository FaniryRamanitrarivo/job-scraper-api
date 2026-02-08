import uuid
from app.engine.step_executor import StepExecutor
from app.engine.context import WorkflowContext

class WorkflowRunner:
    def __init__(self, executor: StepExecutor, browser):
        self.executor = executor
        self.browser = browser

    def run(self, workflow: dict, run_id: str = ''):
        run_id = run_id or str(uuid.uuid4())
        ctx = workflow.get("ctx") or WorkflowContext(run_id, self.browser)
        try:
            for idx, step in enumerate(workflow["steps"], start=1):
                ctx.log(f"Step {idx}: {step['type']}")
                self.executor.execute(step, ctx)
            return {
                "run_id": run_id,
                "data": ctx.data,
                "logs": ctx.logs,
            }
        finally:
            ctx.close()
