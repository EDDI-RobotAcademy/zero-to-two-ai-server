from pydantic import BaseModel
from typing import Optional

from modules.app_user.application.dto.user_dto import UserInfo  # ← app_user에서 가져옴

class GetAccessTokenRequest(BaseModel):
    code: str
    state: Optional[str] = None


class AccessToken(BaseModel):
    access_token: str
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None


class GoogleLoginResult(BaseModel):
    user: UserInfo           # ← auth가 user 도메인의 DTO를 사용
    access_token: str
    refresh_token: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    access_token: str
