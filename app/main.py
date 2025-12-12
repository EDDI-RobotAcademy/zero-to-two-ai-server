"""FastAPI 엔트리포인트: DI/bootstrap 및 라우터 등록."""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.auth.adapter.input.web.auth_router import router as auth_router
from modules.tenant.adapter.input.web.tenant_request_router import router as tenant_request_router
from modules.pipeline.adapter.input.web.router.pipeline_router import router as pipeline_router
from modules.pipeline.adapter.input.web.router.tenant_recommend_router import router as tenant_recommend_router
from modules.system.adapter.input.web.router.health_router import router as health_router
from app.api.routes.tenant import router as llm_router
from shared.infrastructure.db.connection import init_pg_pool
from shared.infrastructure.config.settings import load_settings


def create_app() -> FastAPI:
    """설정 로딩 → CORS → 라우터 등록까지 한 번에 구성."""
    load_dotenv()
    settings = load_settings()

    app = FastAPI(
        title="Zero to Two AI Server",
        description="Google OAuth + JWT 인증 시스템",
        version="1.0.0",
    )

    frontend_origin = os.getenv("FRONTEND_URL", "http://localhost:3000")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin, "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록 (헬스/로그인/테넌트/파이프라인/LLM)
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(tenant_request_router)
    app.include_router(pipeline_router, prefix="/pipeline")
    app.include_router(tenant_recommend_router)
    app.include_router(llm_router)

    @app.on_event("startup")
    def on_startup():
        # DB 커넥션 풀 초기화 (파이프라인 모듈에서 사용)
        init_pg_pool()

    app.state.settings = settings
    return app


app = create_app()


def main() -> None:
    """로컬 개발 실행용 진입점."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=True,
    )


if __name__ == "__main__":
    main()
