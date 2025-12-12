from __future__ import annotations
from typing import Iterable, Sequence
from modules.real_estate.application.dto.fetch_and_store_dto import RealEstateUpsertModel
from abc import ABC, abstractmethod

class RealEstateReadPort(ABC):
    """매물 상세 조회용"""

    @abstractmethod
    def fetch_by_ids(self, ids: Iterable[int]) -> Sequence[RealEstateRecord]:
        """real_estate_list_id -> 매물 DTO 매핑 반환"""
        raise NotImplementedError
