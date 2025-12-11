# modules/auth/application/usecase/google_oauth2_handler.py
from modules.auth.application.dto.auth_dto import GetAccessTokenRequest, GoogleLoginResult
from modules.auth.adapter.output.google_oauth2_service import GoogleOAuth2Service
from modules.app_user.application.dto.user_dto import UserInfo
from typing import Dict

class GoogleOAuth2Handler:
    def __init__(self, service: GoogleOAuth2Service, user_repository, token_service):
        self.service = service
        self.user_repository = user_repository
        self.token_service = token_service

    def get_authorization_url(self, user_type: str | None = None) -> str:
        state = None
        if user_type:
            state = f"user_type={user_type}"
        return self.service.get_authorization_url(state)

    def login(self, code: str, state: str | None = None, user_type: str | None = None) -> GoogleLoginResult:
        # 1) 구글 토큰 교환
        token_req = GetAccessTokenRequest(code=code, state=state)
        google_token = self.service.exchange_code_for_token(token_req)

        # 2) 프로필 조회
        profile = self.service.fetch_user_profile(google_token)
        email = profile.get("email")
        name = profile.get("name") or profile.get("given_name") or ""
        nickname = profile.get("nickname") or name

        # 3) DB에서 user 조회 / 없으면 생성 (app_user 스키마 반영)
        user = self.user_repository.find_by_email(email)
        if user is None:
            user = self.user_repository.create_user(
                name=name,
                nickname=nickname,
                phone=None,
                email=email,
                signup_type="GOOGLE",
                user_type=(user_type or "tenant")
            )
        else:
            # 같은 이메일인데 user_type 다르면 정책에 따라 차단
            if user.get("user_type") != (user_type or user.get("user_type")):
                raise ValueError("다른 유형의 계정으로 로그인 할 수 없습니다.")

        # 4) 서비스 토큰 발급 (access + refresh)
        access, refresh = self.token_service.create_tokens(user["user_id"])

        # 5) UserInfo DTO 구성
        user_info = UserInfo(
            id=user["user_id"],
            email=user["email"],
            nickname=user["nickname"],
            user_type=user["user_type"]
        )

        return GoogleLoginResult(
            user=user_info,
            access_token=access,
            refresh_token=refresh
        )
