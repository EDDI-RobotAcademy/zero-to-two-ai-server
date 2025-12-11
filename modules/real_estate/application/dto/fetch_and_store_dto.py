from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence


@dataclass
class FetchAndStoreCommand:
    """크롤링 입력 조건."""

    item_ids: Sequence[int] | None = None
    region: str | None = None
    limit: int | None = None

    def has_no_filter(self) -> bool:
        return not self.item_ids and not self.region


@dataclass
class FetchAndStoreResult:
    """크롤링 + 저장 결과."""

    fetched: int
    stored: int
    skipped: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class RealEstateUpsertModel:
    """ORM 저장에 필요한 필드만 담는 모델."""

    source_name: str = "zigbang"
    source_id: str = ""
    real_estate_list_id: int | None = None  # DB PK는 자동 생성
    address: str | None = None
    title: str | None = None
    area: float | None = None
    floor: int | None = None
    deal_type: str | None = None
    cost: int | None = None
    manage_cost: str | None = None
    room_count: int | None = None
    amenities: Mapping | None = None
    detailed_explanation: str | None = None
    manage_cost_includes: Mapping | None = None
    manage_cost_not_includes: Mapping | None = None
    options: Mapping | None = None
    nearby_pois: Mapping | None = None
    view_count: int | None = None
    residence_type: str | None = None
    bathroom_count: int | None = None
    movein_available_date: str | None = None
    facing: str | None = None
    parking_available: bool | None = None
    parking_count: int | None = None
    elevator: bool | None = None
    deposit: int | None = None
    rent_fee: int | None = None
    first_create_dt: str | None = None
    last_update_dt: str | None = None
