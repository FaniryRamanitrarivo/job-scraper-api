def fetch_urls(step, ctx):
    selector = step["selector"]
    save_as = step["save_as"]

    ctx.log(f"Fetching URLs using selector: {selector}")

    elements = ctx.browser.find_elements(selector)
    urls = [el.get_attribute("href") for el in elements if el]

    ctx.data[save_as] = urls
    ctx.log(f"Fetched {len(urls)} URLs -> saved as '{save_as}'")
