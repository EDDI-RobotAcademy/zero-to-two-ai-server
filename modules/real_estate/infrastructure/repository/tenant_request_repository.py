from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy import text
from sqlalchemy.orm import Session

from modules.real_estate.application.dto.tenant_request_dto import (
    CreateTenantRequestCommand,
    CreateTenantRequestResult,
)
from modules.real_estate.application.port_out.tenant_request_port import (
    TenantRequestEmbeddingWritePort,
    TenantRequestWritePort,
)
from modules.real_estate.infrastructure.orm.tenant_request_orm import TenantRequestORM
from shared.infrastructure.db.postgres import get_db_session


class TenantRequestRepository(TenantRequestWritePort, TenantRequestEmbeddingWritePort):
    """임차인 요청 저장 + 임베딩 저장 리포지토리."""

    def __init__(self, session_factory=get_db_session):
        self._session_factory = session_factory

    def create_request(
        self, cmd: CreateTenantRequestCommand
    ) -> CreateTenantRequestResult:
        session: Session = self._session_factory()
        now = datetime.utcnow()
        try:
            payload = {
                "user_id": cmd.user_id,
                "budget": cmd.budget,
                "preferred_area": cmd.preferred_area,
                "family": cmd.family,
                "age_range": cmd.age_range,
                "job": cmd.job,
                "commute_location": cmd.commute_location,
                "car_parking": cmd.car_parking,
                "pet": cmd.pet,
                "school_district": cmd.school_district,
                "lifestyle": cmd.lifestyle,
                "expire_dt": cmd.expire_dt,
                "first_create_dt": now,
                "last_update_dt": now,
            }
            obj = TenantRequestORM(**payload)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return CreateTenantRequestResult(
                tenant_request_id=obj.tenant_request_id, embedded=False
            )
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def upsert_embeddings(self, items: Iterable[tuple[int, list[float]]]) -> int:
        session: Session = self._session_factory()
        now = datetime.utcnow()
        saved = 0
        try:
            for tenant_request_id, vector in items:
                update_sql = text(
                    """
                    UPDATE tenant_request_embedding
                    SET embedding = :embedding, last_update_dt = :now
                    WHERE tenant_request_id = :id
                    """
                )
                result = session.execute(
                    update_sql,
                    {"id": tenant_request_id, "embedding": vector, "now": now},
                )
                if result.rowcount == 0:
                    insert_sql = text(
                        """
                        INSERT INTO tenant_request_embedding (tenant_request_id, embedding, first_create_dt, last_update_dt)
                        VALUES (:id, :embedding, :now, :now)
                        """
                    )
                    session.execute(
                        insert_sql,
                        {"id": tenant_request_id, "embedding": vector, "now": now},
                    )
                saved += 1
            session.commit()
            return saved
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
