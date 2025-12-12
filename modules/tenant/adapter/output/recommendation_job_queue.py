from __future__ import annotations

from modules.tenant.application.port.recommendation_job_queue import RecommendationJobQueue


class InMemoryRecommendationJobQueue(RecommendationJobQueue):
    def __init__(self) -> None:
        self.enqueued: list[tuple[str, str]] = []

    def enqueue(self, rental_request_id: str, tenant_id: str) -> None:
        self.enqueued.append((rental_request_id, tenant_id))