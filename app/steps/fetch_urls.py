from app.engine.context import WorkflowContext

def fetch_urls(step: dict, ctx: WorkflowContext):
    selector = step.get("selector")
    save_as = step.get("save_as")

    if not selector:
        raise ValueError("fetch_urls step requires a 'selector' key")
    if not save_as:
        raise ValueError("fetch_urls step requires a 'save_as' key")

    ctx.log(f"Fetching URLs using selector: {selector}")

    elements = ctx.browser.find_elements(selector)
    if not elements:
        ctx.log(f"No elements found for selector '{selector}'", level="WARNING")
        urls = []
    else:
        urls = [el.get_attribute("href") for el in elements]

    ctx.data[save_as] = urls
    ctx.log(f"Fetched {len(urls)} URLs -> saved as '{save_as}'")
