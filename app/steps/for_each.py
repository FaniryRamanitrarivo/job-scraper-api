from app.engine.context import WorkflowContext
from typing import Dict, Callable


def for_each(step: Dict, ctx: WorkflowContext, dispatcher: Dict[str, Callable]):
    collection_name = step["collection"]
    steps_to_run = step["steps"]
    as_object = step.get("as_object")

    items = ctx.data.get(collection_name)
    if not isinstance(items, list):
        raise ValueError(f"Collection '{collection_name}' is not a list")

    ctx.log(f"for_each on '{collection_name}' ({len(items)} items)")

    for index, item in enumerate(items):
        ctx.log(f"for_each item {index} started")

        # Contexte courant
        ctx.current_item = item

        # Création de l'objet métier si demandé
        if as_object:
            ctx.current_object = {"url": item}

        for sub_step in steps_to_run:
            step_type = sub_step["type"]
            handler = dispatcher.get(step_type)

            if not handler:
                ctx.log(f"Unknown step type: {step_type}", level="ERROR")
                continue

            try:
                handler(sub_step, ctx)
            except Exception as e:
                ctx.log(
                    f"Step '{step_type}' failed on item {index}: {e}",
                    level="ERROR"
                )

        # Fin d’itération → on stocke l’objet
        if as_object and ctx.current_object is not None:
            ctx.data.setdefault(f"{as_object}s", []).append(ctx.current_object)
            ctx.current_object = None

        ctx.current_item = None
        ctx.log(f"for_each item {index} finished")
