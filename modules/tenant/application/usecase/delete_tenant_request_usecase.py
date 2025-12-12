"""
Delete Tenant Request Usecase
임차인 요청 삭제 유스케이스
"""
from modules.tenant.application.port.tenant_request_repository_port import TenantRequestRepositoryPort


class DeleteTenantRequestUsecase:
    """임차인 요청 삭제 유스케이스"""

    def __init__(self, repository: TenantRequestRepositoryPort):
        self.repository = repository

    def execute(self, request_id: int, user_id: int) -> bool:
        """
        임차인 요청 삭제 실행

        Args:
            request_id: 요청 ID
            user_id: 인증된 사용자 ID

        Returns:
            삭제 성공 여부

        Raises:
            ValueError: 요청이 존재하지 않을 때
            PermissionError: 소유자가 아닌 경우
        """
        # 기존 엔티티 조회
        domain_entity = self.repository.find_by_id(request_id)

        if not domain_entity:
            raise ValueError(f"임차인 요청을 찾을 수 없습니다: {request_id}")

        # 권한 확인: 본인의 요청만 삭제 가능
        if not domain_entity.is_owned_by(user_id):
            raise PermissionError("본인의 요청만 삭제할 수 있습니다")

        # Repository를 통한 삭제
        return self.repository.delete(request_id)
