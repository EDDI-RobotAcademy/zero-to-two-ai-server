"""규칙 기반 요약기 (네트워크 없이 동작)."""
from __future__ import annotations

import re
from typing import Sequence

from modules.real_estate.application.dto.embedding_dto import (
    RealEstateRecord,
    SummarizeResult,
)
from modules.real_estate.application.port_out.summarizer_port import SummarizerPort


class RuleBasedSummarizer(SummarizerPort):
    """간단한 필드 결합으로 3~5문단 요약."""

    def summarize(self, records: Sequence[RealEstateRecord]) -> Sequence[SummarizeResult]:
        results: list[SummarizeResult] = []
        for record in records:
            parts = []
            parts.append(f"제목: {self._clean(record.title) or '제목 없음'}")
            if record.address:
                parts.append(f"주소: {self._clean(record.address)}")
            price = []
            if record.deal_type:
                price.append(self._clean(record.deal_type))
            if record.deposit is not None:
                price.append(f"보증금 {record.deposit}")
            if record.rent_fee is not None:
                price.append(f"월세 {record.rent_fee}")
            if price:
                parts.append(" / ".join(price))
            if record.area:
                parts.append(f"면적(m2): {record.area}")
            if record.residence_type:
                parts.append(f"주거유형: {self._clean(record.residence_type)}")
            if record.options:
                opts = (
                    ", ".join(map(str, record.options))
                    if isinstance(record.options, list)
                    else str(record.options)
                )
                parts.append(f"옵션: {self._clean(opts)}")
            if record.amenities:
                ams = (
                    ", ".join(map(str, record.amenities))
                    if isinstance(record.amenities, list)
                    else str(record.amenities)
                )
                parts.append(f"주변환경: {self._clean(ams)}")
            if record.description:
                parts.append(f"설명: {self._clean(record.description)}")
            text = "\n".join(parts)
            results.append(SummarizeResult(record_id=record.real_estate_list_id, text=text))
        return results

    @staticmethod
    def _clean(value: str | None) -> str:
        if not value:
            return ""
        # 이모지/특수문자 제거, 숫자/한글/영문/기본 문장부호/공백만 허용
        text = re.sub(r"[^0-9a-zA-Z가-힣\\s.,;:!?'\"()\\-]", " ", value)
        # 연속 공백 정리
        return re.sub(r"\\s+", " ", text).strip()
