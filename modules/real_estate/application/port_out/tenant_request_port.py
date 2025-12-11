from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from modules.real_estate.application.dto.tenant_request_dto import (
    CreateTenantRequestCommand,
    CreateTenantRequestResult,
)


class TenantRequestWritePort(ABC):
    """임차인 요청 저장."""

    @abstractmethod
    def create_request(self, cmd: CreateTenantRequestCommand) -> CreateTenantRequestResult:
        raise NotImplementedError


class TenantRequestEmbeddingWritePort(ABC):
    """임차인 요청 임베딩 저장."""

    @abstractmethod
    def upsert_embeddings(self, items: Iterable[tuple[int, list[float]]]) -> int:
        raise NotImplementedError
