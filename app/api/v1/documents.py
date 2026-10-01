from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.schemas.chunking import ChunkingStrategy
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

document_service = DocumentService()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Query(default=ChunkingStrategy.RECURSIVE),
) -> DocumentResponse:

    try:
        text = await document_service.extract_text(file)
        chunks = document_service.chunk_text(text=text, strategy=chunking_strategy)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return DocumentResponse(
        filename=file.filename or "unknown",
        file_type=file.content_type or "unknown",
        chunking_strategy=chunking_strategy,
        chunks=chunks,
    )
