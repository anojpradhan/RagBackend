from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

document_service = DocumentService()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentResponse:

    try:
        text = await document_service.extract_text(file)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return DocumentResponse(
        filename=file.filename or "unknown",
        file_type=file.content_type or "unknown",
        text=text,
    )
