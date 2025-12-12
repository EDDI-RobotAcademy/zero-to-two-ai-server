from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence, Optional, List

from modules.real_estate.application.dto.fetch_and_store_dto import (
    RealEstateUpsertModel,
)
from modules.real_estate.domain.real_estate import RealEstate


class RealEstateRepositoryPort(ABC):
    """부동산 매물을 영속화/조회하는 Port."""

    @abstractmethod
    def upsert_batch(self, items: Sequence[RealEstateUpsertModel]) -> int:
        """여러 건을 upsert 하고 저장된 건수를 반환한다."""
        raise NotImplementedError

    @abstractmethod
    def exists_source_ids(self, source_name: str, source_ids: Iterable[str]) -> set[str]:
        """이미 저장된 source_id 집합을 반환한다."""
        raise NotImplementedError

    """
        임차인 관점에서 매물을 조회하기 위한 Repository Port
        (일반 필터링 기반 검색용)
        """

    @abstractmethod
    def search_for_tenant(
            self,
            preferred_area: Optional[str],
            min_area: Optional[float],
            room_count: Optional[int],
            bathroom_count: Optional[int],
            deal_type: Optional[str],
            budget: Optional[int],
            limit: int,
    ) -> List[RealEstate]:
        """
        임차인 조건 기반 매물 검색

        - preferred_area: 선호 지역 (구 단위)
        - min_area: 최소 면적
        - room_count: 최소 방 개수
        - bathroom_count: 최소 욕실 개수
        - deal_type: 전세 / 월세 / 매매
        - budget: 예산 상한
        - limit: 최대 조회 개수
        """
        raise NotImplementedError