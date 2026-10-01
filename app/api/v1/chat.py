from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.container import rag_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    try:
        answer = await rag_service.answer(
            session_id=request.session_id,
            question=request.question,
            db=db,
        )

        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat request.",
        ) from exc
