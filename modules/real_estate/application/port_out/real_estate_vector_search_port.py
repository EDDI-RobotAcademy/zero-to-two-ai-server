from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence


@dataclass
class VectorSearchHit:
    real_estate_list_id: int
    score: float


class RealEstateVectorSearchPort(ABC):
    """매물 임베딩 벡터를 대상으로 유사도 검색을 수행."""

    @abstractmethod
    def search(self, vector: Sequence[float], limit: int = 5) -> Sequence[VectorSearchHit]:
        """유사 매물 ID와 점수를 반환."""
        raise NotImplementedError