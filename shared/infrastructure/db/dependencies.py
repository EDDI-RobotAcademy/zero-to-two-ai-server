from typing import Generator
from threading import Lock

from sqlalchemy.orm import Session

from shared.infrastructure.db.postgres import SessionLocal
from shared.infrastructure.db.redis_client import get_redis_client

_redis_lock = Lock()
_redis_instance = None


def get_db() -> Generator[Session, None, None]:
    """FastAPI 요청 단위로 DB 세션을 생성/정리한다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Thread-safe Redis 의존성 (전역 싱글톤 재사용)."""
    global _redis_instance
    if _redis_instance is None:
        with _redis_lock:
            if _redis_instance is None:
                _redis_instance = get_redis_client()
    return _redis_instance
