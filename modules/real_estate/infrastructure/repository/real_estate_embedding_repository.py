from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable, Sequence

from sqlalchemy import text
from sqlalchemy.orm import Session

from modules.real_estate.application.dto.embedding_dto import RealEstateRecord
from modules.real_estate.application.port_out.real_estate_embedding_port import (
    RealEstateEmbeddingReadPort,
    RealEstateEmbeddingWritePort,
)
from modules.real_estate.infrastructure.orm.real_estate_orm import RealEstateORM
from shared.infrastructure.db.postgres import get_db_session


class RealEstateEmbeddingRepository(
    RealEstateEmbeddingReadPort, RealEstateEmbeddingWritePort
):
    """임베딩 대상 조회 및 결과 저장용 리포지토리."""

    def __init__(self, session_factory=get_db_session):
        self._session_factory = session_factory

    def fetch_all_records(self) -> Sequence[RealEstateRecord]:
        session: Session = self._session_factory()
        try:
            rows = session.query(RealEstateORM).all()
            return [self._to_record(row) for row in rows]
        finally:
            session.close()

    def upsert_embeddings(self, items: Iterable[tuple[int, list[float]]]) -> int:
        session: Session = self._session_factory()
        now = datetime.utcnow()
        saved = 0
        try:
            for real_estate_list_id, vector in items:
                # 먼저 업데이트 시도
                update_sql = text(
                    """
                    UPDATE real_estate_list_embedding
                    SET embedding = :embedding, last_update_dt = :now
                    WHERE real_estate_list_id = :id
                    """
                )
                result = session.execute(
                    update_sql,
                    {"id": real_estate_list_id, "embedding": vector, "now": now},
                )
                if result.rowcount == 0:
                    insert_sql = text(
                        """
                        INSERT INTO real_estate_list_embedding (real_estate_list_id, embedding, first_create_dt, last_update_dt)
                        VALUES (:id, :embedding, :now, :now)
                        """
                    )
                    session.execute(
                        insert_sql,
                        {"id": real_estate_list_id, "embedding": vector, "now": now},
                    )
                saved += 1
            session.commit()
            return saved
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _to_record(self, row: RealEstateORM) -> RealEstateRecord:
        return RealEstateRecord(
            real_estate_list_id=row.real_estate_list_id,
            title=row.title,
            address=row.address,
            description=row.detailed_explanation,
            deal_type=row.deal_type,
            deposit=row.deposit,
            rent_fee=row.rent_fee,
            residence_type=row.residence_type,
            area=row.area,
            options=self._parse_json_field(row.options),
            amenities=self._parse_json_field(row.amenities),
        )

    def _parse_json_field(self, value):
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return None
