"""
Update Tenant Request Usecase
임차인 요청 수정 유스케이스
"""
from modules.tenant.application.port.tenant_request_repository_port import TenantRequestRepositoryPort
from modules.tenant.application.dto.tenant_request_dto import TenantRequestUpdateDTO, TenantRequestResponseDTO


class UpdateTenantRequestUsecase:
    """임차인 요청 수정 유스케이스"""

    def __init__(self, repository: TenantRequestRepositoryPort):
        self.repository = repository

    def execute(self, request_id: int, user_id: int, dto: TenantRequestUpdateDTO) -> TenantRequestResponseDTO:
        """
        임차인 요청 수정 실행

        Args:
            request_id: 요청 ID
            user_id: 인증된 사용자 ID
            dto: 수정 요청 DTO

        Returns:
            수정된 임차인 요청 응답 DTO

        Raises:
            ValueError: 요청이 존재하지 않을 때
            PermissionError: 소유자가 아닌 경우
        """
        # 기존 엔티티 조회
        domain_entity = self.repository.find_by_id(request_id)

        if not domain_entity:
            raise ValueError(f"임차인 요청을 찾을 수 없습니다: {request_id}")

        # 권한 확인: 본인의 요청만 수정 가능
        if not domain_entity.is_owned_by(user_id):
            raise PermissionError("본인의 요청만 수정할 수 있습니다")

        # DTO의 값으로 도메인 엔티티 업데이트 (None이 아닌 필드만)
        if dto.budget is not None:
            domain_entity.update_budget(dto.budget)

        if dto.preferred_area is not None:
            domain_entity.update_preferred_area(dto.preferred_area)

        if dto.residence_type is not None:
            domain_entity.residence_type = dto.residence_type

        if dto.deal_type is not None:
            domain_entity.deal_type = dto.deal_type

        if dto.area is not None:
            domain_entity.area = dto.area

        if dto.room_count is not None:
            domain_entity.room_count = dto.room_count

        if dto.bathroom_count is not None:
            domain_entity.bathroom_count = dto.bathroom_count

        if dto.movein_available_date is not None:
            domain_entity.movein_available_date = dto.movein_available_date

        if dto.family is not None:
            domain_entity.family = dto.family

        if dto.age_range is not None:
            domain_entity.age_range = dto.age_range

        if dto.job is not None:
            domain_entity.job = dto.job

        if dto.commute_location is not None:
            domain_entity.commute_location = dto.commute_location

        if dto.car_parking is not None:
            domain_entity.car_parking = dto.car_parking

        if dto.pet is not None:
            domain_entity.pet = dto.pet

        if dto.school_district is not None:
            domain_entity.school_district = dto.school_district

        if dto.extra_information is not None:
            domain_entity.extra_information = dto.extra_information

        # Repository를 통한 영속화
        updated = self.repository.update(domain_entity)

        # Domain Entity -> Response DTO
        return TenantRequestResponseDTO.from_domain(updated)
