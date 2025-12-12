# modules/tenant/application/dto/tenant_request_recommend_dto.py

from typing import Optional
from pydantic import BaseModel, Field


class TenantRequestRecommendDTO(BaseModel):
    """
    임차인 추천 매물 조회 요청 DTO
    - 프론트에서 '추천 매물 보기' 클릭 시 전달
    """

    preferred_area: Optional[str] = Field(
        None, description="선호 지역 (예: 마포구, 영등포구)"
    )
    area: Optional[float] = Field(
        None, description="최소 면적 (㎡ 이상)"
    )
    room_count: Optional[int] = Field(
        None, description="최소 방 개수"
    )
    bathroom_count: Optional[int] = Field(
        None, description="최소 욕실 개수"
    )
    deal_type: Optional[str] = Field(
        None, description="거래 유형 (전세/월세/매매)"
    )
    budget: Optional[int] = Field(
        None,
        description="""
        예산 상한
        - 전세/월세: 보증금 기준
        - 매매: 매매가 기준
        """,
    )
    limit: Optional[int] = Field(
        20, description="조회할 최대 매물 개수"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "preferred_area": "마포구",
                "area": 84,
                "room_count": 3,
                "bathroom_count": 2,
                "deal_type": "전세",
                "budget": 820000000,
                "limit": 20,
            }
        }
