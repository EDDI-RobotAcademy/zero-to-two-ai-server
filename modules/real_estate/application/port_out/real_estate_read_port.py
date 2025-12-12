from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from modules.real_estate.application.dto.embedding_dto import RealEstateRecord


class RealEstateReadPort(ABC):
    """매물 상세 조회 포트."""

    @abstractmethod
    def fetch_by_ids(self, ids: Iterable[int]) -> Sequence[RealEstateRecord]:
        raise NotImplementedError
