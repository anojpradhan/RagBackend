from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.bookings import router as booking_router
from app.api.v1.documents import router as document_router
from app.api.v1.health import router as health_router
from app.db.init_db import init_db
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize PostgreSQL
    await init_db()

    # Initialize Qdrant collection
    embedding_service = EmbeddingService()
    vector_service = VectorService()

    sample_embedding = embedding_service.embed_text("Palm Mind AI")

    vector_service.create_collection(vector_size=len(sample_embedding))

    yield


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
    booking_router,
    prefix="/api/v1",
)

app.include_router(
    document_router,
    prefix="/api/v1",
)
