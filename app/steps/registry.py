from app.steps.open import open_page
from app.steps.fetch_text import fetch_text
from app.steps.fetch_urls import fetch_urls
from app.steps.for_each import for_each

# Le dispatcher centralisé
STEP_HANDLERS = {
    "open": open_page,
    "fetch_text": fetch_text,
    "fetch_urls": fetch_urls,
    "for_each": lambda step, ctx: for_each(step, ctx, STEP_HANDLERS),
}
