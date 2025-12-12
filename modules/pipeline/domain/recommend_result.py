from dataclasses import dataclass

@dataclass
class RecommendRequest:
    tenant_request_id: int
    payload: str
    status: str = "REQUESTED"