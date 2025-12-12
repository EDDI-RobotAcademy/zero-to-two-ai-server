"""
Create Tenant Request Usecase
임차인 요청 생성 유스케이스
"""
from modules.tenant.domain.tenant_request import TenantRequest
from modules.tenant.application.port.tenant_request_repository_port import TenantRequestRepositoryPort
from modules.tenant.application.dto.tenant_request_dto import TenantRequestCreateDTO, TenantRequestResponseDTO


class CreateTenantRequestUsecase:
    """임차인 요청 생성 유스케이스"""

    def __init__(self, repository: TenantRequestRepositoryPort):
        self.repository = repository

    def execute(self, user_id: int, dto: TenantRequestCreateDTO) -> TenantRequestResponseDTO:
        """
        임차인 요청 생성 실행

        Args:
            user_id: 인증된 사용자 ID
            dto: 생성 요청 DTO

        Returns:
            생성된 임차인 요청 응답 DTO

        Raises:
            ValueError: 도메인 규칙 위반 시
        """
        # DTO -> Domain Entity
        domain_entity = TenantRequest(
            tenant_request_id=None,
            user_id=user_id,
            preferred_area=dto.preferred_area,
            residence_type=dto.residence_type,
            deal_type=dto.deal_type,
            budget=dto.budget,
            area=dto.area,
            room_count=dto.room_count,
            bathroom_count=dto.bathroom_count,
            movein_available_date=dto.movein_available_date,
            family=dto.family,
            age_range=dto.age_range,
            job=dto.job,
            commute_location=dto.commute_location,
            car_parking=dto.car_parking,
            pet=dto.pet,
            school_district=dto.school_district,
            extra_information=dto.extra_information
        )

        # Repository를 통한 영속화
        created = self.repository.create(domain_entity)

        # Domain Entity -> Response DTO
        return TenantRequestResponseDTO.from_domain(created)

