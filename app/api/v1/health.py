from fastapi import APIRouter

# making a simple router
router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "Ok"}
