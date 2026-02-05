def open_page(step, ctx):
    url = step["url"]
    ctx.log(f"Opening page: {url}")
    ctx.browser.open(url)
