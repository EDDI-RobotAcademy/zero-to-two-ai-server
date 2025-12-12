import os
import redis
from threading import Lock

_redis_client = None
_redis_lock = Lock()


def get_redis_client():
    """Redis 클라이언트 싱글톤"""
    global _redis_client
    if _redis_client is None:
        with _redis_lock:
            if _redis_client is None:
                _redis_client = redis.Redis(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", 6379)),
                    db=int(os.getenv("REDIS_DB", 0)),
                    password=os.getenv("REDIS_PASSWORD", None),
                    decode_responses=False,
                )
    return _redis_client
