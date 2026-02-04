import time
import uuid
from app.engine import steps

def run_workflow(workflow: dict):
    run_id = str(uuid.uuid4())
    logs = []
    results = {}

    logs.append(f"[{run_id}] Starting workflow on {workflow.get('entry')}")

    for step in workflow.get("steps", []):
        step_type = step.get("type")

        try:
            if step_type == "categories":
                results["categories"] = steps.fetch_urls(step, run_id)
            elif step_type == "listing":
                results["listing"] = steps.fetch_urls(step, run_id)
            elif step_type == "details":
                results["details"] = steps.fetch_urls(step, run_id)
            else:
                logs.append(f"[{run_id}] Unknown step type: {step_type}")
        except Exception as e:
            logs.append(f"[{run_id}] Error in step {step_type}: {e}")

    logs.append(f"[{run_id}] Workflow finished")

    return run_id, logs, results
        