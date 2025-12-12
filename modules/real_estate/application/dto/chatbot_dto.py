from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ChatbotSearchCommand:
    """자연어 메시지와 검색 옵션을 포함하는 입력 DTO."""

    message: str
    top_k: int | None = None


@dataclass
class ChatbotSearchListing:
    """프론트로 내려줄 매물 카드 정보."""

    id: int
    score: float | None = None
    title: str | None = None
    address: str | None = None
    deal_type: str | None = None
    deposit: int | None = None
    rent: int | None = None
    area: float | None = None


@dataclass
class ChatbotSearchResult:
    """챗봇 검색 최종 응답값"""

    query: str
    summary: str
    results: List[ChatbotSearchListing]