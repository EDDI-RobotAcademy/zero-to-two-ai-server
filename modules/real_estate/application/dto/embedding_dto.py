from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass
class RealEstateRecord:
    """임베딩 대상 매물 기본 데이터."""

    real_estate_list_id: int
    title: str | None
    address: str | None
    description: str | None
    deal_type: str | None
    deposit: int | None
    rent_fee: int | None
    residence_type: str | None
    area: float | None
    options: Mapping | None
    amenities: Mapping | None


@dataclass
class SummarizeRequest:
    records: Sequence[RealEstateRecord]
    max_paragraphs: int = 5


@dataclass
class SummarizeResult:
    record_id: int
    text: str


@dataclass
class EmbedRequest:
    record_id: int
    text: str


@dataclass
class EmbedResult:
    record_id: int
    vector: list[float]
