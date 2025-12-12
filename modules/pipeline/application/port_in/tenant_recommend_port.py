from abc import ABC, abstractmethod

class TenantRecommendPort(ABC):

    @abstractmethod
    def execute(self, tenant_request_id: int, request_payload: str) -> dict:
        pass