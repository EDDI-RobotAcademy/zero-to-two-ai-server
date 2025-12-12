"""FastAPI 서버 설정 및 라우터 등록"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.auth.adapter.input.web.auth_router import router as auth_router
from modules.tenant.adapter.input.web.tenant_request_router import router as tenant_request_router
import os

# FastAPI 앱 생성
app = FastAPI(
    title="Zero to Two AI Server",
    description="Google OAuth + JWT 인증 시스템",
    version="1.0.0"
)

# CORS 설정 (프론트엔드와 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,  # 쿠키 전송 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(tenant_request_router)

# 헬스체크 엔드포인트
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Zero to Two AI Server is running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 개발 모드: 코드 변경 시 자동 재시작
    )
