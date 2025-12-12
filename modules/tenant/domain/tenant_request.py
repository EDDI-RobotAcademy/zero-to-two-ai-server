"""
Tenant Request Domain Entity
임차인 요청 도메인 엔티티 (순수 비즈니스 로직)
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class TenantRequest:
    """임차인 매물 요청 도메인 엔티티"""

    tenant_request_id: Optional[int]
    user_id: int
    budget: int

    # 매물 조건
    preferred_area: Optional[str] = None
    residence_type: Optional[str] = None
    deal_type: Optional[str] = None
    area: Optional[float] = None
    room_count: Optional[int] = None
    bathroom_count: Optional[int] = None
    movein_available_date: Optional[date] = None

    # 개인 정보
    family: Optional[str] = None
    age_range: Optional[str] = None
    job: Optional[str] = None
    commute_location: Optional[str] = None

    # 부가 옵션
    car_parking: Optional[bool] = None
    pet: Optional[bool] = None
    school_district: Optional[bool] = None
    extra_information: Optional[str] = None

    # 메타 정보
    first_create_dt: Optional[datetime] = None
    last_update_dt: Optional[datetime] = None

    def __post_init__(self):
        """도메인 불변성 검증"""
        if self.budget <= 0:
            raise ValueError("예산은 0보다 커야 합니다")
        if self.area is not None and self.area <= 0:
            raise ValueError("면적은 0보다 커야 합니다")
        if self.room_count is not None and self.room_count < 0:
            raise ValueError("방 개수는 0 이상이어야 합니다")
        if self.bathroom_count is not None and self.bathroom_count < 0:
            raise ValueError("욕실 개수는 0 이상이어야 합니다")

    def is_owned_by(self, user_id: int) -> bool:
        """요청이 특정 사용자 소유인지 확인"""
        return self.user_id == user_id

    def update_budget(self, new_budget: int) -> None:
        """예산 업데이트"""
        if new_budget <= 0:
            raise ValueError("예산은 0보다 커야 합니다")
        self.budget = new_budget

    def update_preferred_area(self, new_area: Optional[str]) -> None:
        """선호 지역 업데이트"""
        self.preferred_area = new_area
