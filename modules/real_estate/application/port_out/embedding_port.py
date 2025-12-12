from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from modules.real_estate.application.dto.embedding_dto import EmbedRequest, EmbedResult


class EmbeddingPort(ABC):
    """텍스트를 벡터로 변환."""

    @abstractmethod
    async def embed(self, requests: Sequence[EmbedRequest]) -> Sequence[EmbedResult]:
        raise NotImplementedError

    @abstractmethod
    def is_dummy(self) -> bool:
        """더미(테스트용) 임베딩인지 여부."""
        raise NotImplementedError
