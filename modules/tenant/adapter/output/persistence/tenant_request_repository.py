"""
SQLAlchemy Tenant Request Repository Implementation
Repository Port의 SQLAlchemy 구현체
"""
from typing import List, Optional, cast
from sqlalchemy.orm import Session
from modules.tenant.application.port.tenant_request_repository_port import TenantRequestRepositoryPort
from modules.tenant.domain.tenant_request import TenantRequest
from modules.tenant.adapter.output.persistence.tenant_request_orm import TenantRequestORM


class TenantRequestRepository(TenantRequestRepositoryPort):
    """SQLAlchemy 기반 임차인 요청 Repository 구현체"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, tenant_request: TenantRequest) -> TenantRequest:
        """임차인 요청 생성"""
        orm_model = TenantRequestORM(
            user_id=tenant_request.user_id,
            preferred_area=tenant_request.preferred_area,
            residence_type=tenant_request.residence_type,
            deal_type=tenant_request.deal_type,
            budget=tenant_request.budget,
            area=tenant_request.area,
            room_count=tenant_request.room_count,
            bathroom_count=tenant_request.bathroom_count,
            movein_available_date=tenant_request.movein_available_date,
            family=tenant_request.family,
            age_range=tenant_request.age_range,
            job=tenant_request.job,
            commute_location=tenant_request.commute_location,
            car_parking=cast(Optional[bool], tenant_request.car_parking),
            pet=cast(Optional[bool], tenant_request.pet),
            school_district=cast(Optional[bool], tenant_request.school_district),
            extra_information=tenant_request.extra_information
        )

        self.db.add(orm_model)
        self.db.commit()
        self.db.refresh(orm_model)

        return self._to_domain(orm_model)

    def find_by_id(self, request_id: int) -> Optional[TenantRequest]:
        """ID로 임차인 요청 조회"""
        orm_model: Optional[TenantRequestORM] = self.db.query(TenantRequestORM).filter(
            TenantRequestORM.tenant_request_id == request_id
        ).first()

        if not orm_model:
            return None

        return self._to_domain(orm_model)

    def find_by_user_id(self, user_id: int) -> List[TenantRequest]:
        """사용자 ID로 임차인 요청 목록 조회"""
        orm_models = self.db.query(TenantRequestORM).filter(
            TenantRequestORM.user_id == user_id
        ).order_by(TenantRequestORM.first_create_dt.desc()).all()

        return [self._to_domain(orm) for orm in orm_models]

    def find_all(self, skip: int = 0, limit: int = 100) -> List[TenantRequest]:
        """모든 임차인 요청 조회 (페이지네이션)"""
        orm_models = self.db.query(TenantRequestORM).order_by(
            TenantRequestORM.first_create_dt.desc()
        ).offset(skip).limit(limit).all()

        return [self._to_domain(orm) for orm in orm_models]

    def update(self, tenant_request: TenantRequest) -> TenantRequest:
        """임차인 요청 수정"""
        orm_model: Optional[TenantRequestORM] = self.db.query(TenantRequestORM).filter(
            TenantRequestORM.tenant_request_id == tenant_request.tenant_request_id
        ).first()

        if not orm_model:
            raise ValueError(f"TenantRequest with id {tenant_request.tenant_request_id} not found")

        # 도메인 엔티티의 값을 ORM 모델에 반영
        orm_model.preferred_area = tenant_request.preferred_area
        orm_model.residence_type = tenant_request.residence_type
        orm_model.deal_type = tenant_request.deal_type
        orm_model.budget = tenant_request.budget
        orm_model.area = tenant_request.area
        orm_model.room_count = tenant_request.room_count
        orm_model.bathroom_count = tenant_request.bathroom_count
        orm_model.movein_available_date = tenant_request.movein_available_date
        orm_model.family = tenant_request.family
        orm_model.age_range = tenant_request.age_range
        orm_model.job = tenant_request.job
        orm_model.commute_location = tenant_request.commute_location
        orm_model.car_parking = cast(Optional[bool], tenant_request.car_parking)
        orm_model.pet = cast(Optional[bool], tenant_request.pet)
        orm_model.school_district = cast(Optional[bool], tenant_request.school_district)
        orm_model.extra_information = tenant_request.extra_information

        self.db.commit()
        self.db.refresh(orm_model)

        return self._to_domain(orm_model)

    def delete(self, request_id: int) -> bool:
        """임차인 요청 삭제"""
        orm_model: Optional[TenantRequestORM] = self.db.query(TenantRequestORM).filter(
            TenantRequestORM.tenant_request_id == request_id
        ).first()

        if not orm_model:
            return False

        self.db.delete(orm_model)
        self.db.commit()
        return True

    @staticmethod
    def _to_domain(orm_model: TenantRequestORM) -> TenantRequest:
        """ORM 모델을 도메인 엔티티로 변환"""
        return TenantRequest(
            tenant_request_id=orm_model.tenant_request_id,
            user_id=orm_model.user_id,
            preferred_area=orm_model.preferred_area,
            residence_type=orm_model.residence_type,
            deal_type=orm_model.deal_type,
            budget=orm_model.budget,
            area=orm_model.area,
            room_count=orm_model.room_count,
            bathroom_count=orm_model.bathroom_count,
            movein_available_date=orm_model.movein_available_date,
            family=orm_model.family,
            age_range=orm_model.age_range,
            job=orm_model.job,
            commute_location=orm_model.commute_location,
            car_parking=cast(Optional[bool], orm_model.car_parking),
            pet=cast(Optional[bool], orm_model.pet),
            school_district=cast(Optional[bool], orm_model.school_district),
            extra_information=orm_model.extra_information,
            first_create_dt=orm_model.first_create_dt,
            last_update_dt=orm_model.last_update_dt
        )
