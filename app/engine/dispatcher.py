# app/engine/dispatcher.py

from app.engine.steps.open import open_page
from app.engine.steps.fetch_urls import fetch_urls
from app.engine.steps.fetch_text import fetch_text
from app.engine.steps.for_each import for_each


STEP_HANDLERS = {
    "open": open_page,
    "fetch_urls": fetch_urls,
    "fetch_text": fetch_text,
    "for_each": for_each,
}
