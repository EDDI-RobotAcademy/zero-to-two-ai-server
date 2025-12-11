from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from modules.real_estate.application.dto.fetch_and_store_dto import (
    RealEstateUpsertModel,
)


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
