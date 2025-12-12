from shared.infrastructure.db.postgres import Base
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Text, Date, DateTime


class TenantRequestORM(Base):
    __tablename__ = "tenant_request"

    tenant_request_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    budget = Column(Integer, nullable=True)
    preferred_area = Column(String(255), nullable=True)
    family = Column(String(100), nullable=True)
    age_range = Column(String(50), nullable=True)
    job = Column(String(100), nullable=True)
    commute_location = Column(String(255), nullable=True)
    car_parking = Column(Boolean, nullable=True)
    pet = Column(Boolean, nullable=True)
    school_district = Column(Boolean, nullable=True)
    lifestyle = Column(Text, nullable=True)
    expire_dt = Column(Date, nullable=True)
    first_create_dt = Column(DateTime, nullable=True)
    last_update_dt = Column(DateTime, nullable=True)
