# modules/tenant/application/usecase/get_recommend_list_usecase.py

from typing import List

from modules.real_estate.application.port_out.real_estate_repository_port import RealEstateRepositoryPort
from modules.tenant.application.dto.tenant_request_recommend_dto import (
    TenantRequestRecommendDTO,
)
from modules.tenant.application.dto.tenant_recommended_real_estate_dto import (
    TenantRecommendedRealEstateDTO,
)


class GetRecommendListUsecase:
    """
    임차인 의뢰서 조건을 기반으로
    일반 필터링 방식의 매물 추천 목록 조회
    """

    def __init__(
        self,
        real_estate_repository_port: RealEstateRepositoryPort,
    ):
        self.real_estate_repository_port = real_estate_repository_port

    def execute(
        self,
        dto: TenantRequestRecommendDTO,
        user_id: int,
    ) -> List[TenantRecommendedRealEstateDTO]:

        return self.real_estate_repository_port.search_for_tenant(
            preferred_area=dto.preferred_area,
            min_area=dto.area,
            room_count=dto.room_count,
            bathroom_count=dto.bathroom_count,
            deal_type=dto.deal_type,
            budget=dto.budget,
            limit=dto.limit or 20,
        )
