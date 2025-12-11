# modules/auth/adapter/input/auth_middleware.py
from fastapi import HTTPException, Depends, Header, Cookie
from modules.auth.application.service.token_service import TokenService
from modules.auth.adapter.input.web.dependencies import get_token_service

async def auth_required(
    authorization: str | None = Header(None),
    token_service: TokenService = Depends(get_token_service),
):
    """
       인증이 필요한 API에서 사용하는 미들웨어.
       Access Token만 검증한다.
       """
    if not authorization:
        raise HTTPException(status_code=401, detail="INVALID_ACCESS_TOKEN")

    token = authorization.replace("Bearer ", "")
    user_id = token_service.verify_access_token(token)

    return user_id

