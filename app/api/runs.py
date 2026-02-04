from fastapi import APIRouter
import uuid
import time
from app.engine.workflow import run_workflow

router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("/test")
def run_test():

    run_id = str(uuid.uuid4())

    logs = [
        "Start run",
        "Open website",
        "Fetch categories",
        "Fetch job links",
        "Runs finished",
    ]

    for log in logs:
        print(f"[{run_id}] {log}")
        time.sleep(0.2)

    return {
        "run_id": run_id,
        "status": "finished",
    }


@router.post("/execute")
def execute_workflow(workflow: dict):
    run_id, logs, results = run_workflow(workflow)
    for log in logs:
        print(log)

    return {
        "run_id": run_id, 
        "logs_count": len(logs),
        "results": results    
    }