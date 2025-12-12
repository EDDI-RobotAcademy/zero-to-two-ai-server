from shared.infrastructure.db.postgres import Base
from sqlalchemy import Column, BigInteger, DateTime
from pgvector.sqlalchemy import Vector


class RealEstateEmbeddingORM(Base):
    __tablename__ = "real_estate_list_embedding"

    real_estate_list_embedding_id = Column(BigInteger, primary_key=True, index=True)
    real_estate_list_id = Column(BigInteger, nullable=False, index=True)
    embedding = Column(Vector(1536), nullable=False)
    first_create_dt = Column(DateTime, nullable=True)
    last_update_dt = Column(DateTime, nullable=True)
