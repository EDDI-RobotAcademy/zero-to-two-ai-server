from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RecommendListingsQuery:
    tenant_request_id: int
    top_n: int = 10


@dataclass
class RecommendedListing:
    real_estate_list_id: int
    score: float


@dataclass
class RecommendResult:
    listings: List[RecommendedListing]


@dataclass
class RecommendedListingDetail:
    real_estate_list_id: int
    score: float
    title: str | None
    address: str | None
    deal_type: str | None
    deposit: int | None
    rent_fee: int | None
    area: float | None
    residence_type: str | None
