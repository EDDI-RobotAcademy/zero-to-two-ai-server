from dataclasses import dataclass

@dataclass
class RecommendResult:
    request_id: int
    result_json: dict