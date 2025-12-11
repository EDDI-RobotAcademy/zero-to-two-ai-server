# modules/auth/application/service/token_service.py
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from modules.auth.application.port.token_repository_port import TokenRepositoryPort


class TokenService:
    """
    Token 정책
      - Access token lifetime: 1 hour
      - Refresh token lifetime: 30 days
    """
    def __init__(self, token_repo: TokenRepositoryPort):
        self.token_repo = token_repo
        self.access_secret = self._get_secret("ACCESS_SECRET")
        self.refresh_secret = self._get_secret("REFRESH_SECRET")
        self.ACCESS_TTL_SECONDS = 60 * 60            # 1시간
        self.REFRESH_TTL_SECONDS = 60 * 60 * 24 * 30 # 30일

    def _get_secret(self, name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"{name} is not set")
        return value

    def _create_token(self, user_id: int, secret: str, expires_in_seconds: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "iat": now,
            "exp": now + timedelta(seconds=expires_in_seconds),
        }
        return jwt.encode(payload, secret, algorithm="HS256")

    def create_tokens(self, user_id: int) -> tuple[str, str]:
        """
        로그인 직후 호출:
          - Access / Refresh 생성
          - Refresh는 Redis에 저장
        """
        access = self._create_token(user_id, self.access_secret, self.ACCESS_TTL_SECONDS)
        refresh = self._create_token(user_id, self.refresh_secret, self.REFRESH_TTL_SECONDS)

        # 기존 refresh 덮어쓰기
        self.token_repo.save_refresh(user_id, refresh, ttl_seconds=self.REFRESH_TTL_SECONDS)

        return access, refresh

    def rotate_refresh(self, refresh_token: str) -> tuple[int, str, str]:
        """
        Refresh 토큰 회전 정책
        """
        try:
            payload = jwt.decode(refresh_token, self.refresh_secret, algorithms=["HS256"])
            user_id = int(payload.get("user_id"))
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="REFRESH_TOKEN_EXPIRED")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="REFRESH_TOKEN_INVALID")

        stored = self.token_repo.get_refresh(user_id)
        if stored is None:
            raise HTTPException(status_code=401, detail="REFRESH_TOKEN_NOT_FOUND")

        if stored != refresh_token:
            self.token_repo.delete_refresh(user_id)
            raise HTTPException(status_code=401, detail="REFRESH_TOKEN_REUSED")

        new_access, new_refresh = self.create_tokens(user_id)
        return user_id, new_access, new_refresh

    def logout(self, user_id: int):
        self.token_repo.delete_refresh(user_id)

    def verify_access_token(self, access_token: str) -> int:
        """
        Authorization 헤더로 들어온 Access Token 검증
        """
        try:
            payload = jwt.decode(access_token, self.access_secret, algorithms=["HS256"])
            return int(payload.get("user_id"))
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="TOKEN_EXPIRED")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="TOKEN_INVALID")

    def get_user_id_from_refresh(self, refresh_token: str) -> int | None:
        try:
            payload = jwt.decode(refresh_token, self.refresh_secret, algorithms=["HS256"])
            return int(payload.get("user_id"))
        except jwt.PyJWTError:
            return None
