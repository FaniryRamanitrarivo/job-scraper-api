def for_each(step, ctx):
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
            try:
                handler = ctx.dispatcher[sub_step["type"]]
                handler(sub_step, ctx)
            except Exception as e:
                ctx.log(
                    f"Step '{sub_step['type']}' failed on item {index}: {e}",
                    level="ERROR",
                )
                continue

        ctx.log(f"for_each item {index} finished")
