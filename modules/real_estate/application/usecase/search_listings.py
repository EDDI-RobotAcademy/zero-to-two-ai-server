from __future__ import annotations

from modules.real_estate.application.dto.search_listing_dto import (
    SearchListingQuery,
    SearchListingResult,
)
from modules.real_estate.application.port_out.real_estate_search_port import (
    RealEstateSearchPort,
)


class SearchListingsService:
    """필터 기반 매물 검색."""

    def __init__(self, search_port: RealEstateSearchPort):
        self.search_port = search_port

    async def execute(self, query: SearchListingQuery) -> list[SearchListingResult]:
        return list(self.search_port.search(query))
