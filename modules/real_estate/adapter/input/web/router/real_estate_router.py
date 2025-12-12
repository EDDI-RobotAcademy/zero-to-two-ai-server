from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

from modules.real_estate.application.dto.search_listing_dto import (
    SearchListingQuery,
)
from modules.real_estate.application.usecase.search_listings import SearchListingsService
from modules.real_estate.infrastructure.repository.real_estate_repository import (
    RealEstateRepository,
)

real_estate_search_router = APIRouter(prefix="/real_estate", tags=["Real Estate Handling"])


class SearchRequest(BaseModel):
    preferred_area: List[str] = []
    area: Optional[float] = None  # 최소 면적(m2)
    room_count: Optional[int] = None
    bathroom_count: Optional[int] = None
    deal_type: Optional[str] = None
    budget: Optional[int] = None


def get_search_service() -> SearchListingsService:
    repo = RealEstateRepository()
    return SearchListingsService(repo)


@real_estate_search_router.post("/search")
async def search_listings(
    req: SearchRequest, service: SearchListingsService = Depends(get_search_service)
):
    query = SearchListingQuery(
        preferred_area=req.preferred_area,
        area=req.area,
        room_count=req.room_count,
        bathroom_count=req.bathroom_count,
        deal_type=req.deal_type,
        budget=req.budget,
    )
    results = await service.execute(query)
    return {"results": [r.__dict__ for r in results]}
