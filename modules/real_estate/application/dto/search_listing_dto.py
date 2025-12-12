from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchListingQuery:
    preferred_area: List[str]
    area: Optional[float] = None  # 최소 면적(m2)
    room_count: Optional[int] = None
    bathroom_count: Optional[int] = None
    deal_type: Optional[str] = None  # 전세/매매/월세
    budget: Optional[int] = None


@dataclass
class SearchListingResult:
    real_estate_list_id: int
    title: str | None
    address: str | None
    deal_type: str | None
    deposit: int | None
    cost: int | None
    area: float | None
    room_count: int | None
    bathroom_count: int | None
