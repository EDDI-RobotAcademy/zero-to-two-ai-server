# modules/auth/adapter/input/web/auth_router.py
import os
from fastapi import APIRouter, Depends, Query, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from modules.auth.adapter.input.web.dependencies import get_google_usecase, get_token_service
from modules.auth.application.dto.auth_dto import TokenRefreshRequest, TokenRefreshResponse

router = APIRouter(prefix="/authentication", tags=["Auth"])

@router.get("/google")
def redirect_to_google(user_type: str = Query(...), google_usecase = Depends(get_google_usecase)):
    """
    프론트는 /auth/google?user_type=landlord 또는 tenant 호출
    """
    url = google_usecase.get_authorization_url(user_type)
    return RedirectResponse(url)


@router.get("/google/redirect")
def google_login(code: str, state: str | None = None, google_usecase = Depends(get_google_usecase)):
    # state에서 user_type 파싱 (Google이 state로 전달함)
    user_type = None
    if state and "user_type=" in state:
        for param in state.split("&"):
            if param.startswith("user_type="):
                user_type = param.split("=", 1)[1]
                break

    result = google_usecase.login(code=code, state=state, user_type=user_type)

    # 환경별 secure flag 설정
    env = os.getenv("ENV", "development")
    secure_flag = True if env == "production" else False

    # 프론트엔드 URL 환경 변수화
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    response = RedirectResponse(frontend_url)
    # HttpOnly refresh token cookie (Rotate 정책에 따라 서버가 새 refresh를 발급/갱신함)
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=secure_flag,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/authentication"  # refresh endpoint 범위
    )

    return response


@router.post("/token/refresh", response_model=TokenRefreshResponse)
def token_refresh(request: Request, token_service = Depends(get_token_service)):
    """
    Refresh 동작 (cookie 기반 A 전략):
      1) 쿠키에서 refresh_token 우선 읽음
      2) 토큰 회전(rotate): 새 access, 새 refresh 발급
      3) 새 refresh는 HttpOnly cookie로 덮어쓰기
      4) 새 access는 body로 반환
    """
    env = os.getenv("ENV", "development")
    secure_flag = True if env == "production" else False

    cookie_refresh = request.cookies.get("refresh_token")
    if not cookie_refresh:
        raise HTTPException(status_code=401, detail="REFRESH_REQUIRED")

    user_id, new_access, new_refresh = token_service.rotate_refresh(cookie_refresh)

    response = JSONResponse({"access_token": new_access})
    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=secure_flag,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/authentication"
    )
    return response


@router.post("/logout")
def logout(request: Request, token_service = Depends(get_token_service)):
    """
    Logout:
      - server-side refresh token 삭제
      - session:{session_id} 삭제 (있다면)
      - client cookie 삭제
    """
    # cookie-based logout flow
    cookie_refresh = request.cookies.get("refresh_token")

    # refresh 기반 로그아웃
    if cookie_refresh:
        user_id = token_service.get_user_id_from_refresh(cookie_refresh)
        if user_id:
            token_service.logout(user_id) # refreshToken 삭제

    # 응답에서 쿠키 제거
    response = JSONResponse({"message": "logged out"})
    response.delete_cookie("refresh_token", path="/authentication")
    return response
