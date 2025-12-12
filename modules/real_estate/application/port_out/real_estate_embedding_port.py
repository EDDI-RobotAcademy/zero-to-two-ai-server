from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from modules.real_estate.application.dto.embedding_dto import RealEstateRecord


class RealEstateEmbeddingReadPort(ABC):
    """임베딩 대상 매물 조회."""

    @abstractmethod
    def fetch_all_records(self) -> Sequence[RealEstateRecord]:
        raise NotImplementedError


class RealEstateEmbeddingWritePort(ABC):
    """임베딩 결과 저장."""

    @abstractmethod
    def upsert_embeddings(self, items: Iterable[tuple[int, list[float]]]) -> int:
        """(real_estate_list_id, vector) 리스트를 저장하고 건수를 반환."""
        raise NotImplementedError
