from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Sequence, Set, Optional, List
import json
from datetime import datetime

from sqlalchemy.orm import Session

from modules.real_estate.application.dto.fetch_and_store_dto import RealEstateUpsertModel
from modules.real_estate.application.port_out.real_estate_repository_port import (
    RealEstateRepositoryPort,
)
from modules.real_estate.application.port_out.real_estate_read_port import (
    RealEstateReadPort,
)
from modules.real_estate.application.port_out.real_estate_search_port import (
    RealEstateSearchPort,
)
from modules.real_estate.application.dto.search_listing_dto import (
    SearchListingQuery,
    SearchListingResult,
)
from modules.real_estate.infrastructure.orm.real_estate_orm import RealEstateORM
from modules.tenant.application.dto.tenant_recommended_real_estate_dto import TenantRecommendedRealEstateDTO
from shared.infrastructure.db.postgres import get_db_session


class RealEstateRepository(RealEstateRepositoryPort, RealEstateReadPort, RealEstateSearchPort):
    """RealEstateRepositoryPort 구현체 - SQLAlchemy 기반."""

    def __init__(self, session_factory=get_db_session):
        self._session_factory = session_factory

    def upsert_batch(self, items: Sequence[RealEstateUpsertModel]) -> int:
        session: Session = self._session_factory()
        stored = 0
        try:
            for model in items:
                payload = self._to_payload(model)
                source_id = payload.get("source_id")
                source_name = payload.get("source_name")
                if not source_id:
                    continue
                existing = (
                    session.query(RealEstateORM)
                    .filter(
                        RealEstateORM.source_id == source_id,
                        RealEstateORM.source_name == source_name,
                    )
                    .one_or_none()
                )
                if existing:
                    for key, value in payload.items():
                        if key == "real_estate_list_id":
                            continue
                        setattr(existing, key, value)
                else:
                    payload.pop("real_estate_list_id", None)
                    session.add(RealEstateORM(**payload))
                stored += 1
            session.commit()
            return stored
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def exists_source_ids(self, source_name: str, source_ids: Iterable[str]) -> Set[str]:
        session: Session = self._session_factory()
        try:
            rows = (
                session.query(RealEstateORM.source_id)
                .filter(
                    RealEstateORM.source_name == source_name,
                    RealEstateORM.source_id.in_(list(source_ids)),
                )
                .all()
            )
            return {row[0] for row in rows}
        finally:
            session.close()

    def fetch_by_ids(self, ids: Iterable[int]) -> Sequence[RealEstateORM]:
        session: Session = self._session_factory()
        try:
            return (
                session.query(RealEstateORM)
                .filter(RealEstateORM.real_estate_list_id.in_(list(ids)))
                .all()
            )
        finally:
            session.close()

    def search(self, query: SearchListingQuery) -> Sequence[SearchListingResult]:
        session: Session = self._session_factory()
        try:
            q = session.query(RealEstateORM)
            if query.preferred_area:
                conds = [
                    RealEstateORM.address.ilike(f"%{area}%")
                    for area in query.preferred_area
                    if area
                ]
                if conds:
                    from sqlalchemy import or_

                    q = q.filter(or_(*conds))
            if query.area is not None:  # 최소 면적
                q = q.filter(RealEstateORM.area >= query.area)
            if query.room_count is not None:
                q = q.filter(RealEstateORM.room_count >= query.room_count)
            if query.bathroom_count is not None:
                q = q.filter(RealEstateORM.bathroom_count >= query.bathroom_count)
            if query.deal_type:
                q = q.filter(RealEstateORM.deal_type == query.deal_type)
            if query.budget is not None:
                if query.deal_type == "매매":
                    q = q.filter(RealEstateORM.cost <= query.budget)
                else:
                    q = q.filter(RealEstateORM.deposit <= query.budget)

            rows = q.limit(100).all()
            return [
                SearchListingResult(
                    real_estate_list_id=row.real_estate_list_id,
                    title=row.title,
                    address=row.address,
                    deal_type=row.deal_type,
                    deposit=row.deposit,
                    cost=row.cost,
                    area=row.area,
                    room_count=row.room_count,
                    bathroom_count=row.bathroom_count,
                )
                for row in rows
            ]
        finally:
            session.close()

    def _to_payload(self, model: RealEstateUpsertModel) -> dict:
        data = asdict(model)
        # amenities 컬럼이 Text 이므로 JSON 문자열로 저장
        if data.get("amenities") is not None:
            data["amenities"] = json.dumps(data["amenities"], ensure_ascii=False)
        # 날짜 문자열을 timestamp 형식으로 변환 시도
        for key in ("first_create_dt", "last_update_dt"):
            data[key] = self._parse_datetime(data.get(key))
        return data

    def _parse_datetime(self, value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        # 지원 포맷 시도
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y.%m.%d %H:%M:%S",
            "%Y.%m.%d",
            "%Y-%m-%d",
            "%Y년 %m월 %d일",
            "%Y년%m월%d일",
            "%Y년 %m월 %d일 %H:%M",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(str(value), fmt)
            except ValueError:
                continue
        return None


    def search_for_tenant(
        self,
        preferred_area: Optional[str],
        min_area: Optional[float],
        room_count: Optional[int],
        bathroom_count: Optional[int],
        deal_type: Optional[str],
        budget: Optional[int],
        limit: int,
    ) -> List[TenantRecommendedRealEstateDTO]:

        session: Session = self._session_factory()
        try:
            query = session.query(RealEstateORM)

            if preferred_area:
                query = query.filter(
                    RealEstateORM.address.contains(preferred_area)
                )

            if min_area:
                query = query.filter(RealEstateORM.area >= min_area)

            if room_count:
                query = query.filter(RealEstateORM.room_count >= room_count)

            if bathroom_count:
                query = query.filter(
                    RealEstateORM.bathroom_count >= bathroom_count
                )

            if deal_type:
                query = query.filter(RealEstateORM.deal_type == deal_type)

            if budget:
                if deal_type in ("전세", "월세"):
                    query = query.filter(RealEstateORM.deposit <= budget)
                elif deal_type == "매매":
                    query = query.filter(RealEstateORM.cost <= budget)

            results = query.limit(limit).all()

            return [
                TenantRecommendedRealEstateDTO(
                    real_estate_id=orm.real_estate_list_id,
                    title=orm.title,
                    area=orm.area,
                    room_count=orm.room_count,
                    bathroom_count=orm.bathroom_count,
                    deal_type=orm.deal_type,
                    cost=orm.cost,
                    deposit=orm.deposit,
                    address=orm.address,
                    description=orm.description,
                )
                for orm in results
            ]
        finally:
            session.close()