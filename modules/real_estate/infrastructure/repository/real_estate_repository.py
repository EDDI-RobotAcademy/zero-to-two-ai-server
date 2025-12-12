from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Sequence, Set
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
from modules.real_estate.infrastructure.orm.real_estate_orm import RealEstateORM
from shared.infrastructure.db.postgres import get_db_session


class RealEstateRepository(RealEstateRepositoryPort, RealEstateReadPort):
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
