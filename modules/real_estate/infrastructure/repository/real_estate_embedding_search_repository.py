from __future__ import annotations

from typing import Iterable, Sequence, Tuple

from sqlalchemy import text
from sqlalchemy.orm import Session

from modules.real_estate.application.port_out.real_estate_embedding_search_port import (
    RealEstateEmbeddingSearchPort,
)
from shared.infrastructure.db.postgres import get_db_session


class RealEstateEmbeddingSearchRepository(RealEstateEmbeddingSearchPort):
    """pgvector 유사도 검색 리포지토리."""

    def __init__(self, session_factory=get_db_session):
        self._session_factory = session_factory

    def search_similar(
        self, query_vector: Iterable[float], top_n: int = 10
    ) -> Sequence[Tuple[int, float]]:
        session: Session = self._session_factory()
        try:
            vec = [float(x) for x in query_vector]
            sql = text(
                """
                SELECT real_estate_list_id, embedding <-> (:vec)::vector AS distance
                FROM real_estate_list_embedding
                ORDER BY distance ASC
                LIMIT :limit
                """
            )
            rows = session.execute(
                sql, {"vec": vec, "limit": top_n}
            ).fetchall()
            return [(row[0], float(row[1])) for row in rows]
        finally:
            session.close()
