# modules/tenant/application/dto/tenant_recommended_real_estate_dto.py

from typing import Optional
from pydantic import BaseModel


class TenantRecommendedRealEstateDTO(BaseModel):
    """
    임차인 추천 매물 응답 DTO
    - tenant 화면에 필요한 정보만 포함
    """

    real_estate_id: int
    title: str
    area: float
    room_count: int
    bathroom_count: int
    deal_type: str
    cost: Optional[int]
    deposit: Optional[int]
    address: str
    description: Optional[str]
