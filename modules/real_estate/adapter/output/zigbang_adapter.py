"""직방 API 응답을 도메인 Upsert 모델로 변환하는 어댑터."""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from modules.real_estate.application.dto.fetch_and_store_dto import RealEstateUpsertModel
from modules.real_estate.application.port_out.zigbang_fetch_port import ZigbangFetchPort


class ZigbangAdapter:
    """ZigbangFetchPort를 감싸 지역 필터 및 상세 조회 후 Upsert 모델을 반환."""

    def __init__(self, fetch_port: ZigbangFetchPort):
        self.fetch_port = fetch_port

    def fetch_and_convert(
        self,
        item_ids: Iterable[int],
        region_filters: Sequence[str] | None = None,
    ) -> Tuple[List[RealEstateUpsertModel], List[str]]:
        """배치 조회 → 지역 필터 → 상세 조회 → 매핑."""
        region_filters = list(region_filters or [])
        errors: List[str] = []
        normalized_ids = self._normalize_item_ids(item_ids)
        if not normalized_ids:
            return [], ["유효한 item_id가 없습니다."]

        try:
            summary_items = self.fetch_port.fetch_by_item_ids(normalized_ids)
        except Exception as exc:  # noqa: BLE001
            return [], [f"배치 조회 실패: {exc}"]

        filtered = self._filter_by_region(summary_items, region_filters)

        converted: List[RealEstateUpsertModel] = []
        for item in filtered:
            item_id = item.get("item_id") or item.get("itemId")
            if not item_id:
                errors.append("item_id 없음")
                continue
            try:
                detail = self.fetch_port.fetch_detail(item_id)
                converted.append(self._map_raw_item_to_upsert_model(detail))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"상세 조회/매핑 실패 {item_id}: {exc}")
        return converted, errors

    def _normalize_item_ids(self, item_ids: Iterable[Any]) -> List[int]:
        normalized: List[int] = []
        for raw in item_ids:
            if isinstance(raw, Mapping):
                val = raw.get("item_id") or raw.get("itemId")
            else:
                val = raw
            try:
                if val is not None:
                    normalized.append(int(val))
            except (TypeError, ValueError):
                continue
        return normalized

    def _filter_by_region(
        self, raw_items: Sequence[Mapping], region_filters: Sequence[str]
    ) -> list[Mapping]:
        if not region_filters:
            return list(raw_items)
        filtered = []
        for item in raw_items:
            full_text = (
                item.get("addressOrigin", {}).get("fullText")
                or item.get("address")
                or ""
            )
            if any(region in full_text for region in region_filters):
                filtered.append(item)
        return filtered

    def _map_raw_item_to_upsert_model(
        self, raw_item: Mapping[str, Any]
    ) -> RealEstateUpsertModel:
        summarized = self._summarize_item(dict(raw_item))
        source_id = summarized.get("source_id")
        if not source_id:
            raise ValueError("source_id(zigbang item_id)가 없습니다.")

        return RealEstateUpsertModel(
            source_name=summarized.get("source_name") or "zigbang",
            source_id=source_id,
            address=summarized.get("address"),
            title=summarized.get("title"),
            area=summarized.get("area"),
            floor=summarized.get("floor"),
            deal_type=summarized.get("deal_type"),
            cost=summarized.get("cost"),
            manage_cost=summarized.get("manage_cost"),
            room_count=summarized.get("room_count"),
            amenities=summarized.get("amenities"),
            detailed_explanation=summarized.get("detailed_explanation"),
            manage_cost_includes=summarized.get("manage_cost_includes"),
            manage_cost_not_includes=summarized.get("manage_cost_not_includes"),
            options=summarized.get("options"),
            nearby_pois=summarized.get("nearby_pois"),
            view_count=summarized.get("view_count"),
            residence_type=summarized.get("residence_type"),
            bathroom_count=summarized.get("bathroom_count"),
            movein_available_date=summarized.get("movein_available_date"),
            facing=summarized.get("facing"),
            parking_available=summarized.get("parking_available"),
            parking_count=summarized.get("parking_count"),
            elevator=summarized.get("elevator"),
            deposit=summarized.get("deposit"),
            rent_fee=summarized.get("rent_fee"),
            first_create_dt=summarized.get("first_create_dt"),
            last_update_dt=summarized.get("last_update_dt"),
        )

    def _summarize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        price = item.get("price", {}) or {}
        area = item.get("area", {}) or {}
        floor_info = item.get("floor", {}) or {}
        manage_cost = item.get("manageCost", {}) or {}
        neighborhoods = item.get("neighborhoods", {}) or {}
        address_origin = item.get("addressOrigin", {}) or {}

        amenities = [a.get("title") for a in neighborhoods.get("amenities", [])]

        poi_whitelist = {"지하철역", "편의점", "대형마트", "버스정류장"}
        nearby_pois = []
        for poi in neighborhoods.get("nearbyPois", []):
            if not poi.get("exists"):
                continue
            if poi.get("poiType") not in poi_whitelist:
                continue
            nearby_pois.append(
                {
                    "종류": poi.get("poiType"),
                    "거리_m": poi.get("distance"),
                    "이동수단": poi.get("transport"),
                    "예상시간_초": poi.get("timeTaken"),
                }
            )

        return {
            "source_name": item.get("itemBmType") or "zigbang",
            "source_id": str(item.get("itemId")),
            "deal_type": item.get("salesType"),
            "residence_type": item.get("residenceType"),
            "deposit": price.get("deposit"),
            "rent_fee": price.get("rent"),
            "cost": price.get("sales"),
            "manage_cost": manage_cost.get("amount"),
            "manage_cost_includes": manage_cost.get("includes", []),
            "manage_cost_not_includes": manage_cost.get("notIncludes", []),
            "area": area.get("전용면적M2"),
            "floor": self._to_int(floor_info.get("floor")),
            "title": item.get("title"),
            "detailed_explanation": item.get("description"),
            "options": item.get("options", []),
            "amenities": amenities,
            "nearby_pois": nearby_pois,
            "address": self._merge_address(
                address_origin.get("fullText"), item.get("jibunAddress")
            ),
            "view_count": item.get("viewCount"),
            "bathroom_count": self._to_int(item.get("bathroomCount")),
            "movein_available_date": item.get("moveinDate"),
            "facing": (
                f"{item.get('directionCriterion')} 기준 {item.get('roomDirection')}"
                if item.get("roomDirection")
                else None
            ),
            "parking_available": bool(item.get("parkingAvailableText"))
            if "parkingAvailableText" in item
            else None,
            "parking_count": self._extract_number(item.get("parkingCountText")),
            "elevator": item.get("elevator"),
            "first_create_dt": item.get("approveDate"),
            "last_update_dt": item.get("updatedAt"),
            "room_count": self._room_type_to_count(item.get("roomType")),
        }

    @staticmethod
    def _to_int(value) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_number(text: Any) -> int | None:
        if text is None:
            return None
        if isinstance(text, (int, float)):
            return int(text)
        m = re.search(r"\d+", str(text))
        return int(m.group()) if m else None

    @staticmethod
    def _room_type_to_count(room_type: str | None) -> int | None:
        mapping = {
            "원룸": 1,
            "투룸": 2,
            "쓰리룸": 3,
        }
        return mapping.get(room_type)

    @staticmethod
    def _merge_address(full_text: str | None, jibun: str | None) -> str:
        if full_text and jibun:
            if jibun.startswith(full_text):
                return jibun.strip()
            if full_text.startswith(jibun):
                return full_text.strip()
            tokens = full_text.split()
            if len(tokens) > 1:
                tail = " ".join(tokens[1:])
                if jibun.startswith(tail):
                    return f"{tokens[0]} {jibun}".strip()
            return f"{full_text} {jibun}".strip()
        return (full_text or jibun or "").strip()
