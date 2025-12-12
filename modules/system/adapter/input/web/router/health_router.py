"""헬스체크 라우터 (adapter/input/web/router)."""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def health_check():
    return {"status": "ok", "message": "Zero to Two AI Server is running"}


@router.get("/health")
def health():
    return {"status": "healthy"}
