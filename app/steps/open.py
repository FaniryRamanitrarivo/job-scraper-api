import time
from selenium.common.exceptions import TimeoutException, WebDriverException

def open_page(step, ctx):
    url = step.get("url") or ctx.data.get("item")
    if not url:
        raise ValueError("open step requires 'url' or item")

    max_retries = step.get("retries", 3)
    base_delay = step.get("retry_delay", 2)  # seconds

    attempt = 0

    while attempt <= max_retries:
        try:
            ctx.log(f"Opening {url} (attempt {attempt + 1})")
            ctx.browser.open(url)
            return  # ✅ succès → on sort

        except (TimeoutException, WebDriverException) as e:
            attempt += 1

            if attempt > max_retries:
                ctx.log(
                    f"Failed to open {url} after {max_retries} retries: {e}",
                    level="ERROR",
                )
                raise

            delay = base_delay * attempt
            ctx.log(
                f"Open failed ({e}), retrying in {delay}s...",
                level="WARNING",
            )
            time.sleep(delay)
