from fastapi import FastAPI

from app.api.v1.documents import router as document_router
from app.api.v1.health import router as health_router

# creating fastapi applicatiopn

app = FastAPI(
    title=" Palm Mind AI- Task",
    version="1.0.0",
    description="Conversational Rag Backend with document ingestion and interview booking",
)
app.include_router(
    document_router,
    prefix="/api/v1",
)
app.include_router(health_router, prefix="/api/v1")
