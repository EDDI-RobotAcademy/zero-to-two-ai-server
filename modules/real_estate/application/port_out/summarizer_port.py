from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from modules.real_estate.application.dto.embedding_dto import (
    RealEstateRecord,
    SummarizeResult,
)


class SummarizerPort(ABC):
    """매물 정보를 요약 텍스트로 변환."""

    @abstractmethod
    def summarize(self, records: Sequence[RealEstateRecord]) -> Sequence[SummarizeResult]:
        raise NotImplementedError
