from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Sequence


class ZigbangFetchPort(ABC):
    """직방에서 매물(raw) 데이터를 가져오는 Port."""

    @abstractmethod
    def fetch_by_item_ids(self, item_ids: Iterable[int]) -> Sequence[Mapping]:
        """item_id 리스트로 매물 raw 데이터를 받아온다."""
        raise NotImplementedError

    @abstractmethod
    def fetch_detail(self, item_id: int) -> Mapping:
        """단건 상세 조회."""
        raise NotImplementedError
