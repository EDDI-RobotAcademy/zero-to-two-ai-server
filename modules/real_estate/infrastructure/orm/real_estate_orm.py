from shared.infrastructure.db.postgres import Base
from sqlalchemy import Column, BigInteger, String, Boolean, Float, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB


class RealEstateORM(Base):
    __tablename__ = "real_estate_list"

    real_estate_list_id = Column(BigInteger, primary_key=True, index=True)
    source_name = Column(String(20), nullable=True)
    source_id = Column(String(20), nullable=True, index=True)
    address = Column(String(100), nullable=True)
    title = Column(String(100), nullable=True)
    area = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    deal_type = Column(String(50), nullable=True)
    cost = Column(BigInteger, nullable=True)
    manage_cost = Column(String(100), nullable=True)
    room_count = Column(Integer, nullable=True)
    amenities = Column(Text, nullable=True)
    detailed_explanation = Column(Text, nullable=True)
    first_create_dt = Column(DateTime, nullable=True)
    last_update_dt = Column(DateTime, nullable=True)
    manage_cost_includes = Column(JSONB, nullable=True)
    manage_cost_not_includes = Column(JSONB, nullable=True)
    options = Column(JSONB, nullable=True)
    nearby_pois = Column(JSONB, nullable=True)
    view_count = Column(Integer, nullable=True)
    residence_type = Column(String(50), nullable=True)
    bathroom_count = Column(Integer, nullable=True)
    movein_available_date = Column(String(100), nullable=True)
    facing = Column(String(100), nullable=True)
    parking_available = Column(Boolean, nullable=True)
    parking_count = Column(Integer, nullable=True)
    elevator = Column(Boolean, nullable=True)
    deposit = Column(BigInteger, nullable=True)
    rent_fee = Column(BigInteger, nullable=True)
