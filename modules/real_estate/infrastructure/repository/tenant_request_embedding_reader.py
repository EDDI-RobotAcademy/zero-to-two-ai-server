from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from modules.real_estate.application.port_out.tenant_request_embedding_port import (
    TenantRequestEmbeddingReadPort,
)
from shared.infrastructure.db.postgres import get_db_session
from modules.real_estate.infrastructure.orm.tenant_request_embedding_orm import (
    TenantRequestEmbeddingORM,
)


class TenantRequestEmbeddingReader(TenantRequestEmbeddingReadPort):
    """tenant_request_embedding에서 벡터를 조회한다."""

    def __init__(self, session_factory=get_db_session):
        self._session_factory = session_factory

    def get_vector(self, tenant_request_id: int) -> Iterable[float] | None:
        session: Session = self._session_factory()
        try:
            row = (
                session.query(TenantRequestEmbeddingORM)
                .filter(TenantRequestEmbeddingORM.tenant_request_id == tenant_request_id)
                .one_or_none()
            )
            if row and row.embedding is not None:
                return [float(x) for x in row.embedding]
            return None
        finally:
            session.close()
