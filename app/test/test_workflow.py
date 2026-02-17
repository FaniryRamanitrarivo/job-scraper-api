from app.engine.workflow_runner import WorkflowRunner
from app.engine.step_executor import StepExecutor
from app.steps.registry import STEP_HANDLERS
from app.browsers.selenium_browser import SeleniumBrowser

browser = SeleniumBrowser()
executor = StepExecutor(STEP_HANDLERS)
runner = WorkflowRunner(executor, browser)

workflow = {
    "steps": [
        {"type": "open", "url": "https://example.com"},
        {"type": "fetch_text", "selector": "h1"}
    ]
}

result = runner.run(workflow)
print(result)
