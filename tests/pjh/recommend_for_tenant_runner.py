"""tenant_request 임베딩 기반 매물 추천 러너 (라우팅 없이 실행)."""
from __future__ import annotations

import os
import sys
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.real_estate.application.dto.recommendation_dto import (
    RecommendListingsQuery,
)
from modules.real_estate.application.usecase.recommend_real_estate_for_tenant import (
    RecommendRealEstateForTenantService,
)
from modules.real_estate.infrastructure.repository.real_estate_embedding_search_repository import (
    RealEstateEmbeddingSearchRepository,
)
from modules.real_estate.infrastructure.repository.tenant_request_embedding_reader import (
    TenantRequestEmbeddingReader,
)
from modules.real_estate.infrastructure.repository.real_estate_repository import (
    RealEstateRepository,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    tenant_reader = TenantRequestEmbeddingReader()
    re_search = RealEstateEmbeddingSearchRepository()
    re_reader = RealEstateRepository()
    usecase = RecommendRealEstateForTenantService(tenant_reader, re_search, re_reader)

    query = RecommendListingsQuery(tenant_request_id=2, top_n=10)
    result = await usecase.execute(query)
    for idx, rec in enumerate(result.listings, start=1):
        logger.info(
            "[%s] id=%s score=%.4f title=%s address=%s deal_type=%s deposit=%s rent=%s area=%s",
            idx,
            rec.real_estate_list_id,
            rec.score,
            rec.title,
            rec.address,
            rec.deal_type,
            rec.deposit,
            rec.rent_fee,
            rec.area,
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
