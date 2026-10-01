from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.chunking import ChunkingStrategy
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()
embedding_service = EmbeddingService()
vector_service = VectorService()
document_repository = DocumentRepository()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Query(default=ChunkingStrategy.RECURSIVE),
    db: AsyncSession = Depends(get_db),
) -> DocumentResponse:

    filename = file.filename or "unknown"
    file_type = file.content_type or "unknown"

    try:
        #Extract text
        text = await document_service.extract_text(file)

        #Chunk text
        chunks = document_service.chunk_text(
            text=text,
            strategy=chunking_strategy,
        )

        #Save document metadata to PostgreSQL
        document = await document_repository.create(
            db,
            filename=filename,
            file_type=file_type,
            chunking_strategy=chunking_strategy,
            chunk_count=len(chunks),
        )

        #Generate embeddings
        embeddings = embedding_service.embed_documents(chunks)

        #Store chunks and embeddings in Qdrant
        vector_service.store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_id=str(document.id),
            filename=filename,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return DocumentResponse(
        filename=filename,
        file_type=file_type,
        chunking_strategy=chunking_strategy,
        chunks=chunks,
    )
