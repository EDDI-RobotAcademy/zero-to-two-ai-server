from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable


class TenantRequestEmbeddingReadPort(ABC):
    """tenant_request 임베딩 조회."""

    @abstractmethod
    def get_vector(self, tenant_request_id: int) -> Iterable[float] | None:
        raise NotImplementedError
