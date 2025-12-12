# modules/auth/dependencies.py

from modules.auth.application.port.token_repository_port import TokenRepositoryPort
from modules.auth.adapter.output.redis_token_repository import RedisTokenRepository
from modules.auth.adapter.output.google_oauth2_service import GoogleOAuth2Service
from modules.auth.application.service.token_service import TokenService
from modules.auth.application.usecase.google_oauth2_handler import GoogleOAuth2Handler
from modules.app_user.adapter.output.app_user_repository import AppUserRepository

from shared.infrastructure.db.redis_client import get_redis_client
from shared.infrastructure.config.settings import load_settings
from shared.infrastructure.db.postgres import SessionLocal


_settings = load_settings()

# DB factory -----------------------------------------
def _get_db_factory():
    return lambda: SessionLocal()


# Redis client ----------------------------------------
_redis_client = None

def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = get_redis_client()
    return _redis_client


# Token Repository (Port → Adapter) --------------------
_token_repo: TokenRepositoryPort | None = None

def get_token_repository() -> TokenRepositoryPort:
    global _token_repo
    if _token_repo is None:
        _token_repo = RedisTokenRepository(get_redis())  # ← Port 구현체(어댑터)
    return _token_repo


# Token Service ---------------------------------------
_token_service = None

def get_token_service() -> TokenService:
    global _token_service
    if _token_service is None:
        _token_service = TokenService(
            token_repo=get_token_repository()     # ← Port 의존
        )
    return _token_service


# Google OAuth Service (외부 서비스 어댑터) -----------
_google_service = None

def get_google_service() -> GoogleOAuth2Service:
    global _google_service
    if _google_service is None:
        _google_service = GoogleOAuth2Service()
    return _google_service


# User Repository (DB adapter) ------------------------
_user_repo = None

def get_user_repository():
    global _user_repo
    if _user_repo is None:
        _user_repo = AppUserRepository(_get_db_factory())
    return _user_repo


# Google OAuth UseCase --------------------------------
_google_handler = None

def get_google_usecase() -> GoogleOAuth2Handler:
    global _google_handler
    if _google_handler is None:
        _google_handler = GoogleOAuth2Handler(
            service=get_google_service(),
            user_repository=get_user_repository(),
            token_service=get_token_service()
        )
    return _google_handler
