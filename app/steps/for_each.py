from app.engine.context import WorkflowContext
from typing import Dict, Callable

def for_each(step: Dict, ctx: WorkflowContext, dispatcher: Dict[str, Callable]):
    collection_name = step["collection"]
    steps_to_run = step["steps"]

    items = ctx.data.get(collection_name, [])
    if not isinstance(items, list):
        raise ValueError(f"Collection '{collection_name}' is not a list")

    ctx.log(f"for_each on '{collection_name}' ({len(items)} items)")

    for index, item in enumerate(items):
        ctx.log(f"for_each item {index} started")
        ctx.data["item"] = item
        ctx.data["item_index"] = index

        for sub_step in steps_to_run:
            step_type = sub_step["type"]
            if step_type not in dispatcher:
                ctx.log(f"Unknown step type: {step_type}", level="ERROR")
                continue

            # Gérer les champs dynamiques
            sub_step_copy = sub_step.copy()
            if sub_step_copy.get("url_from_item"):
                sub_step_copy["url"] = item
            if sub_step_copy.get("save_as_from_item"):
                sub_step_copy["save_as"] = f"{sub_step_copy['save_as_from_item']}_{index}"

            try:
                dispatcher[step_type](sub_step_copy, ctx)
            except Exception as e:
                ctx.log(f"Step '{step_type}' failed on item {index}: {e}", level="ERROR")

        ctx.log(f"for_each item {index} finished")
