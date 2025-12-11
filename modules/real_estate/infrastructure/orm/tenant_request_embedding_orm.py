from shared.infrastructure.db.postgres import Base
from sqlalchemy import Column, BigInteger, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY


class TenantRequestEmbeddingORM(Base):
    __tablename__ = "tenant_request_embedding"

    tenant_request_embedding_id = Column(BigInteger, primary_key=True, index=True)
    tenant_request_id = Column(BigInteger, nullable=False, index=True)
    embedding = Column(ARRAY(Float), nullable=False)
    first_create_dt = Column(DateTime, nullable=True)
    last_update_dt = Column(DateTime, nullable=True)
