"""
Tenant Request ORM Model
SQLAlchemy 테이블 정의
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float, Date
from sqlalchemy.sql import func
from shared.infrastructure.db.postgres import Base


class TenantRequestORM(Base):
    """임차인 요청 ORM 모델"""

    __tablename__ = "tenant_request"

    tenant_request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.user_id"), nullable=False, index=True)

    # 매물 조건
    preferred_area = Column(String(200), nullable=True)
    residence_type = Column(String(50), nullable=True)  # apartment, officetel, villa 등
    deal_type = Column(String(50), nullable=True)  # jeonse, monthly, sale
    budget = Column(Integer, nullable=False)
    area = Column(Float, nullable=True)  # 평수
    room_count = Column(Integer, nullable=True)
    bathroom_count = Column(Integer, nullable=True)
    movein_available_date = Column(Date, nullable=True)

    # 개인 정보
    family = Column(String(100), nullable=True)
    age_range = Column(String(50), nullable=True)
    job = Column(String(100), nullable=True)
    commute_location = Column(String(200), nullable=True)

    # 부가 옵션
    car_parking = Column(Boolean, nullable=True)
    pet = Column(Boolean, nullable=True)
    school_district = Column(Boolean, nullable=True)
    extra_information = Column(Text, nullable=True)

    # 메타 정보
    first_create_dt = Column(DateTime, server_default=func.now(), nullable=False)
    last_update_dt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
