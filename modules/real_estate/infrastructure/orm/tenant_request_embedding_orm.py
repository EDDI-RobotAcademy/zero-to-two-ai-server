from shared.infrastructure.db.postgres import Base
from sqlalchemy import Column, BigInteger, DateTime
from pgvector.sqlalchemy import Vector


class TenantRequestEmbeddingORM(Base):
    __tablename__ = "tenant_request_embedding"

    tenant_request_embedding_id = Column(BigInteger, primary_key=True, index=True)
    tenant_request_id = Column(BigInteger, nullable=False, index=True)
    embedding = Column(Vector(1536), nullable=False)
    first_create_dt = Column(DateTime, nullable=True)
    last_update_dt = Column(DateTime, nullable=True)
