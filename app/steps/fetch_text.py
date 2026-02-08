# app/steps/fetch_text.py
from app.engine.context import WorkflowContext

def fetch_text(step: dict, ctx: WorkflowContext):
    selector = step["selector"]
    field = step["save_as"]

    text = ctx.browser.get_text(selector)

    if ctx.current_object is not None:
        ctx.current_object[field] = text
    else:
        ctx.data[field] = text
