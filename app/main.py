from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.documents import router as document_router
from app.api.v1.health import router as health_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# create fast api

app = FastAPI(
    title="Palm Mind AI - RAG Backend",
    version="1.0.0",
    description=(
        "Conversational RAG backend with document ingestion and interview booking."
    ),
    lifespan=lifespan,
)


app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    document_router,
    prefix="/api/v1",
)
