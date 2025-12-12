from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from modules.real_estate.application.dto.search_listing_dto import (
    SearchListingQuery,
    SearchListingResult,
)


class RealEstateSearchPort(ABC):
    """매물 검색 포트."""

    @abstractmethod
    def search(self, query: SearchListingQuery) -> Sequence[SearchListingResult]:
        raise NotImplementedError
