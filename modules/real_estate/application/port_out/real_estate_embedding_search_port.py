from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence, Tuple


class RealEstateEmbeddingSearchPort(ABC):
    """매물 임베딩 유사도 검색."""

    @abstractmethod
    def search_similar(
        self, query_vector: Iterable[float], top_n: int = 10
    ) -> Sequence[Tuple[int, float]]:
        """(real_estate_list_id, distance/score) 리스트 반환."""
        raise NotImplementedError
