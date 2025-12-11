# modules/auth/adapter/output/redis_token_repository.py
import json
from typing import Optional
from redis.exceptions import RedisError
from fastapi import HTTPException

from modules.auth.application.port.token_repository_port import TokenRepositoryPort


class RedisTokenRepository(TokenRepositoryPort):
    def __init__(self, redis_client):
        self.redis = redis_client

    # refresh token 저장/조회/삭제 (토큰 재발급용)
    def save_refresh(self, user_id: int, refresh_token: str, ttl_seconds: int = 60 * 60 * 24 * 30):
        try:
            self.redis.set(f"refresh:{user_id}", refresh_token, ex=ttl_seconds)
        except RedisError as e:
            raise HTTPException(status_code=503, detail="REDIS_UNAVAILABLE") from e

    def get_refresh(self, user_id: int) -> Optional[str]:
        data = self.redis.get(f"refresh:{user_id}")
        if not data:
            return None
        # redis.get returns bytes if decode_responses=False
        return data.decode() if isinstance(data, (bytes, bytearray)) else data

    def delete_refresh(self, user_id: int):
        self.redis.delete(f"refresh:{user_id}")
