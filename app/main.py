from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.routes.workflow import router as workflow_router
from app.api.routes.scraping import router as scraping_router

app = FastAPI()

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(workflow_router)
app.include_router(scraping_router)
