"""
Get Tenant Request Usecase
임차인 요청 조회 유스케이스
"""
from typing import List, Optional
from modules.tenant.application.port.tenant_request_repository_port import TenantRequestRepositoryPort
from modules.tenant.application.dto.tenant_request_dto import TenantRequestResponseDTO


class GetTenantRequestUsecase:
    """임차인 요청 조회 유스케이스"""

    def __init__(self, repository: TenantRequestRepositoryPort):
        self.repository = repository

    def execute_by_id(self, request_id: int, user_id: int) -> Optional[TenantRequestResponseDTO]:
        """
        ID로 임차인 요청 단건 조회

        Args:
            request_id: 요청 ID
            user_id: 인증된 사용자 ID

        Returns:
            임차인 요청 응답 DTO 또는 None

        Raises:
            PermissionError: 소유자가 아닌 경우
        """
        domain_entity = self.repository.find_by_id(request_id)

        if not domain_entity:
            return None

        # 권한 확인: 본인의 요청만 조회 가능
        if not domain_entity.is_owned_by(user_id):
            raise PermissionError("본인의 요청만 조회할 수 있습니다")

        return self._to_response_dto(domain_entity)

    def execute_by_user(self, user_id: int) -> List[TenantRequestResponseDTO]:
        """
        사용자 ID로 임차인 요청 목록 조회

        Args:
            user_id: 인증된 사용자 ID

        Returns:
            임차인 요청 응답 DTO 리스트
        """
        domain_entities = self.repository.find_by_user_id(user_id)
        return [self._to_response_dto(entity) for entity in domain_entities]

    def execute_all(self, skip: int = 0, limit: int = 100) -> List[TenantRequestResponseDTO]:
        """
        모든 임차인 요청 조회 (관리자용)

        Args:
            skip: 건너뛸 개수
            limit: 최대 조회 개수

        Returns:
            임차인 요청 응답 DTO 리스트
        """
        domain_entities = self.repository.find_all(skip, limit)
        return [self._to_response_dto(entity) for entity in domain_entities]

    @staticmethod
    def _to_response_dto(domain_entity) -> TenantRequestResponseDTO:
        """도메인 엔티티를 응답 DTO로 변환"""
        return TenantRequestResponseDTO.from_domain(domain_entity)
