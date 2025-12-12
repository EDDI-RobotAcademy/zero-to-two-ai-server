"""
Tenant Request DTO
API 요청/응답 데이터 전송 객체
"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


# =========================
# Create DTO
# =========================
class TenantRequestCreateDTO(BaseModel):
    """임차인 요청 생성 DTO"""

    # 매물 조건
    preferred_area: Optional[str] = Field(None, description="선호 지역", max_length=200)
    residence_type: Optional[str] = Field(None, description="주거 유형 (apartment, officetel, villa)", max_length=50)
    deal_type: Optional[str] = Field(None, description="거래 유형 (jeonse, monthly, sale)", max_length=50)
    budget: int = Field(..., description="예산", gt=0)
    area: Optional[float] = Field(None, description="면적(평수)", gt=0)
    room_count: Optional[int] = Field(None, description="방 개수", ge=0)
    bathroom_count: Optional[int] = Field(None, description="욕실 개수", ge=0)
    movein_available_date: Optional[date] = Field(None, description="입주 가능일")

    # 개인 정보
    family: Optional[str] = Field(None, description="가족 구성", max_length=100)
    age_range: Optional[str] = Field(None, description="연령대", max_length=50)
    job: Optional[str] = Field(None, description="직업", max_length=100)
    commute_location: Optional[str] = Field(None, description="출퇴근 위치", max_length=200)

    # 부가 옵션
    car_parking: Optional[bool] = Field(None, description="주차 가능 여부")
    pet: Optional[bool] = Field(None, description="반려동물 가능 여부")
    school_district: Optional[bool] = Field(None, description="학군 고려 여부")
    extra_information: Optional[str] = Field(None, description="추가 정보")

    class Config:
        json_schema_extra = {
            "example": {
                "preferred_area": "강남구",
                "residence_type": "apartment",
                "deal_type": "jeonse",
                "budget": 50000000,
                "area": 70,
                "room_count": 3,
                "bathroom_count": 2,
                "movein_available_date": "2024-09-01",
                "family": "3인 가족",
                "age_range": "30대",
                "job": "회사원",
                "commute_location": "역삼역",
                "car_parking": True,
                "pet": False,
                "school_district": True,
                "extra_information": "조용한 환경 선호"
            }
        }


# =========================
# Update DTO
# =========================
class TenantRequestUpdateDTO(BaseModel):
    """임차인 요청 수정 DTO"""

    # 매물 조건
    preferred_area: Optional[str] = Field(None, max_length=200)
    residence_type: Optional[str] = Field(None, max_length=50)
    deal_type: Optional[str] = Field(None, max_length=50)
    budget: Optional[int] = Field(None, gt=0)
    area: Optional[float] = Field(None, gt=0)
    room_count: Optional[int] = Field(None, ge=0)
    bathroom_count: Optional[int] = Field(None, ge=0)
    movein_available_date: Optional[date] = None

    # 개인 정보
    family: Optional[str] = Field(None, max_length=100)
    age_range: Optional[str] = Field(None, max_length=50)
    job: Optional[str] = Field(None, max_length=100)
    commute_location: Optional[str] = Field(None, max_length=200)

    # 부가 옵션
    car_parking: Optional[bool] = None
    pet: Optional[bool] = None
    school_district: Optional[bool] = None
    extra_information: Optional[str] = None


# =========================
# ID Response DTO (생성/수정 응답용)
# =========================
class TenantRequestIdResponseDTO(BaseModel):
    """임차인 요청 ID 응답 DTO"""
    tenant_request_id: int


# =========================
# Summary DTO (목록 조회용)
# =========================
class TenantRequestSummaryDTO(BaseModel):
    """임차인 요청 요약 DTO (목록 조회용)"""

    tenant_request_id: int
    preferred_area: Optional[str]
    residence_type: Optional[str]
    deal_type: Optional[str]
    budget: int

    class Config:
        from_attributes = True


# =========================
# Response DTO
# =========================
class TenantRequestResponseDTO(BaseModel):
    """임차인 요청 응답 DTO"""

    tenant_request_id: int
    user_id: int

    # 매물 조건
    preferred_area: Optional[str]
    residence_type: Optional[str]
    deal_type: Optional[str]
    budget: int
    area: Optional[float]
    room_count: Optional[int]
    bathroom_count: Optional[int]
    movein_available_date: Optional[date]

    # 개인 정보
    family: Optional[str]
    age_range: Optional[str]
    job: Optional[str]
    commute_location: Optional[str]

    # 부가 옵션
    car_parking: Optional[bool]
    pet: Optional[bool]
    school_district: Optional[bool]
    extra_information: Optional[str]

    # 메타 정보
    first_create_dt: datetime
    last_update_dt: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, domain):
        return cls(
            tenant_request_id=domain.tenant_request_id,
            user_id=domain.user_id,
            preferred_area=domain.preferred_area,
            residence_type=domain.residence_type,
            deal_type=domain.deal_type,
            budget=domain.budget,
            area=domain.area,
            room_count=domain.room_count,
            bathroom_count=domain.bathroom_count,
            movein_available_date=domain.movein_available_date,
            family=domain.family,
            age_range=domain.age_range,
            job=domain.job,
            commute_location=domain.commute_location,
            car_parking=domain.car_parking,
            pet=domain.pet,
            school_district=domain.school_district,
            extra_information=domain.extra_information,
            first_create_dt=domain.first_create_dt,
            last_update_dt=domain.last_update_dt,
        )
