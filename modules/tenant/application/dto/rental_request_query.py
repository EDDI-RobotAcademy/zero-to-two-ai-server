from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RecommendationItem:
    listing_id: str
    title: str
    summary: str
    matched_score: float


@dataclass
class RecommendationResult:
    rental_request_id: str
    items: List[RecommendationItem]
    generated_reason: Optional[str] = None