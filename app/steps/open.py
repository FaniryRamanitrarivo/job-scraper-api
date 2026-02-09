import time
from selenium.common.exceptions import TimeoutException, WebDriverException


def open_page(step: dict, ctx):
    url = step.get("url") or ctx.current_item
    if not url:
        raise ValueError("open step requires 'url' or current item")

    max_retries = step.get("retries", 3)
    base_delay = step.get("retry_delay", 2)

    for attempt in range(1, max_retries + 2):
        try:
            ctx.log(f"Opening {url} (attempt {attempt})")

            # ✅ on passe par TON wrapper
            ctx.browser.open(url)

            return  # succès

        except TimeoutException:
            ctx.log(
                "Page load timeout ignored (DOM likely usable)",
                level="WARNING",
            )
            return

        except WebDriverException as e:
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
