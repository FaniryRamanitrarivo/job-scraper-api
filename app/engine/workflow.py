from app.engine.context import WorkflowContext
from app.engine.dispatcher import STEP_HANDLERS
import uuid

def run_workflow(workflow, run_id=None):
    run_id = run_id or str(uuid.uuid4())
    ctx = WorkflowContext(run_id, dispatcher=STEP_HANDLERS)  # 🔹 dispatcher injecté

    try:
        for index, step in enumerate(workflow["steps"], start=1):
            step_type = step["type"]

            if step_type not in STEP_HANDLERS:
                raise ValueError(f"Unknown step type: {step_type}")

            ctx.log(f"Step {index}: {step_type}")
            STEP_HANDLERS[step_type](step, ctx)

        return {
            "run_id": run_id,
            "data": ctx.data,
            "logs": ctx.logs,
        }

    finally:
        ctx.close()
