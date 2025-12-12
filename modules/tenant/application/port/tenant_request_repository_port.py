"""
Tenant Request Repository Port (Interface)
Repository의 추상 인터페이스 정의
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from modules.tenant.domain.tenant_request import TenantRequest


class TenantRequestRepositoryPort(ABC):
    """임차인 요청 Repository 인터페이스"""

    @abstractmethod
    def create(self, tenant_request: TenantRequest) -> TenantRequest:
        """
        임차인 요청 생성

        Args:
            tenant_request: 생성할 임차인 요청 도메인 엔티티

        Returns:
            생성된 임차인 요청 (ID 포함)
        """
        pass

    @abstractmethod
    def find_by_id(self, request_id: int) -> Optional[TenantRequest]:
        """
        ID로 임차인 요청 조회

        Args:
            request_id: 요청 ID

        Returns:
            임차인 요청 도메인 엔티티 또는 None
        """
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[TenantRequest]:
        """
        사용자 ID로 임차인 요청 목록 조회

        Args:
            user_id: 사용자 ID

        Returns:
            임차인 요청 도메인 엔티티 리스트
        """
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[TenantRequest]:
        """
        모든 임차인 요청 조회 (페이지네이션)

        Args:
            skip: 건너뛸 개수
            limit: 최대 조회 개수

        Returns:
            임차인 요청 도메인 엔티티 리스트
        """
        pass

    @abstractmethod
    def update(self, tenant_request: TenantRequest) -> TenantRequest:
        """
        임차인 요청 수정

        Args:
            tenant_request: 수정할 임차인 요청 도메인 엔티티

        Returns:
            수정된 임차인 요청
        """
        pass

    @abstractmethod
    def delete(self, request_id: int) -> bool:
        """
        임차인 요청 삭제

        Args:
            request_id: 요청 ID

        Returns:
            삭제 성공 여부
        """
        pass