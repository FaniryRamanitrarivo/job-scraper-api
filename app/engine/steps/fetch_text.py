def fetch_text(step, ctx):
    selector = step["selector"]
    save_as = step["save_as"]

    ctx.log(f"Fetching text using selector: {selector}")

    text = ctx.browser.get_text(selector)
    ctx.data[save_as] = text
