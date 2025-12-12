from __future__ import annotations

from typing import Protocol


class RecommendationJobQueue(Protocol):
    def enqueue(self, rental_request_id: str, tenant_id: str) -> None:
        ...