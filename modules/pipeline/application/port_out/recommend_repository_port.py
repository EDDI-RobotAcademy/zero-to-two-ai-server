from abc import ABC, abstractmethod
from typing import Dict

class RecommendRepositoryPort(ABC):

    @abstractmethod
    def save_request(self, tenant_request_id: int, request_payload: str) -> int:
        pass

    @abstractmethod
    def update_status(self, request_id: int, status: str):
        pass

    @abstractmethod
    def save_result(self, request_id: int, result_json: Dict):
        pass