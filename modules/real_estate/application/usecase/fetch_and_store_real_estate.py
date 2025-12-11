from __future__ import annotations

from typing import Mapping, Sequence

from modules.real_estate.adapter.output.zigbang_adapter import ZigbangAdapter
from modules.real_estate.application.dto.fetch_and_store_dto import (
    FetchAndStoreCommand,
    FetchAndStoreResult,
    RealEstateUpsertModel,
)
from modules.real_estate.application.port_in.fetch_and_store_real_estate_port import (
    FetchAndStoreRealEstatePort,
)
from modules.real_estate.application.port_out.real_estate_repository_port import (
    RealEstateRepositoryPort,
)
from modules.real_estate.application.port_out.zigbang_fetch_port import ZigbangFetchPort


class FetchAndStoreRealEstateService(FetchAndStoreRealEstatePort):
    """직방 크롤링 → 정제 → 저장 유스케이스."""

    def __init__(
        self,
        fetch_port: ZigbangFetchPort,
        repository_port: RealEstateRepositoryPort,
        region_filters: list[str] | None = None,
    ):
        self.fetch_port = fetch_port
        self.repository_port = repository_port
        self.region_filters = region_filters or []
        self.adapter = ZigbangAdapter(fetch_port)

    def execute(self, command: FetchAndStoreCommand) -> FetchAndStoreResult:
        if command.has_no_filter():
            return FetchAndStoreResult(
                fetched=0, stored=0, skipped=0, errors=["크롤링 조건이 없습니다."]
            )

        raw_items = self._fetch_raw_items(command)
        fetched = len(raw_items)
        if fetched == 0:
            return FetchAndStoreResult(fetched=0, stored=0, skipped=0, errors=[])

        prepared_models, errors = self.adapter.fetch_and_convert(
            raw_items, self.region_filters
        )

        existing_ids = (
            self.repository_port.exists_source_ids(
                source_name=prepared_models[0].source_name or "zigbang",
                source_ids=[m.source_id for m in prepared_models if m.source_id],
            )
            if prepared_models
            else set()
        )

        to_store = [m for m in prepared_models if m.source_id not in existing_ids]
        skipped = len(prepared_models) - len(to_store)

        stored = self.repository_port.upsert_batch(to_store) if to_store else 0

        return FetchAndStoreResult(
            fetched=fetched, stored=stored, skipped=skipped, errors=errors
        )

    def _fetch_raw_items(self, command: FetchAndStoreCommand) -> Sequence[Mapping]:
        if command.item_ids:
            return self.fetch_port.fetch_by_item_ids(command.item_ids)
        if command.region:
            return self.fetch_port.fetch_by_region(command.region, command.limit)
        return []
