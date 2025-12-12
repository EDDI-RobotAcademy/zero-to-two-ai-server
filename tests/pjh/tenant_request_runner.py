"""임차인 요청 생성 + 임베딩 파이프라인 테스트 러너."""
from __future__ import annotations

import os
import sys
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.real_estate.application.dto.tenant_request_dto import (
    CreateTenantRequestCommand,
)
from modules.real_estate.application.usecase.create_tenant_request import (
    CreateTenantRequestService,
)
from modules.real_estate.infrastructure.repository.tenant_request_repository import (
    TenantRequestRepository,
)
from modules.real_estate.infrastructure.external.embedding_agent import (
    OpenAIEmbeddingAgent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    repo = TenantRequestRepository()
    embedder = OpenAIEmbeddingAgent()
    usecase = CreateTenantRequestService(repo, repo, embedder)

    cmd = CreateTenantRequestCommand(
        user_id=1,
        budget=20000,
        preferred_area="서울시 마포구",
        family="4인 가족",
        age_range="50대",
        job="변호사",
        commute_location="역삼",
        car_parking=True,
        pet=True,
        school_district=True,
        lifestyle="조용하고 산책을 즐깁니다.",
        expire_dt=None,
    )
    result = await usecase.execute(cmd)
    logger.info("tenant_request_id=%s embedded=%s", result.tenant_request_id, result.embedded)
    if embedder.is_dummy():
        logger.warning("임베딩이 더미 모드로 실행되었습니다 (OPENAI_API_KEY 미설정).")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
