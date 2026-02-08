from fastapi import APIRouter
from app.engine.workflow_runner import WorkflowRunner
from app.engine.step_executor import StepExecutor
from app.steps.registry import STEP_HANDLERS
from app.browser.selenium_browser import SeleniumBrowser

router = APIRouter(prefix="/workflow", tags=["workflow"])

executor = StepExecutor(STEP_HANDLERS)
browser = SeleniumBrowser()  # headless par défaut
runner = WorkflowRunner(executor, browser)

@router.post("/execute")
def execute_workflow(workflow: dict):
    browser = SeleniumBrowser() 
    executor = StepExecutor(STEP_HANDLERS)
    runner = WorkflowRunner(executor, browser)

    try:
        result = runner.run(workflow)
        return {
            "run_id": result["run_id"],
            "logs_count": len(result["logs"]),
            "results": result["data"]
        }
    finally:
        browser.close() 
