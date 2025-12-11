from __future__ import annotations

from abc import ABC, abstractmethod

from modules.real_estate.application.dto.fetch_and_store_dto import (
    FetchAndStoreCommand,
    FetchAndStoreResult,
)


class FetchAndStoreRealEstatePort(ABC):
    """크롤링 + 저장 유스케이스를 노출하는 입력 포트."""

    @abstractmethod
    def execute(self, command: FetchAndStoreCommand) -> FetchAndStoreResult:
        raise NotImplementedError
