"""필터 기반 매물 검색 러너 (라우팅 없이 실행)."""
from __future__ import annotations

import os
import sys
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.real_estate.application.dto.search_listing_dto import SearchListingQuery
from modules.real_estate.application.usecase.search_listings import SearchListingsService
from modules.real_estate.infrastructure.repository.real_estate_repository import (
    RealEstateRepository,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    repo = RealEstateRepository()
    service = SearchListingsService(repo)
    query = SearchListingQuery(
        preferred_area=["영등포구", "마포구", "용산구"],
        area=10.0,
        room_count=None,
        bathroom_count=None,
        deal_type="전세",
        budget=50000,
    )
    results = await service.execute(query)
    for idx, r in enumerate(results, start=1):
        logger.info(
            "[%s] id=%s title=%s address=%s deal=%s deposit=%s cost=%s area=%s room=%s bath=%s",
            idx,
            r.real_estate_list_id,
            r.title,
            r.address,
            r.deal_type,
            r.deposit,
            r.cost,
            r.area,
            r.room_count,
            r.bathroom_count,
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
