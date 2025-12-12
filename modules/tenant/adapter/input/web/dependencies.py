"""
Tenant Request Dependencies
의존성 주입을 위한 팩토리 함수들
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from shared.infrastructure.db.postgres import get_db_session
from modules.tenant.adapter.output.persistence.tenant_request_repository import TenantRequestRepository
from modules.tenant.application.usecase.create_tenant_request_usecase import CreateTenantRequestUsecase
from modules.tenant.application.usecase.get_tenant_request_usecase import GetTenantRequestUsecase
from modules.tenant.application.usecase.update_tenant_request_usecase import UpdateTenantRequestUsecase
from modules.tenant.application.usecase.delete_tenant_request_usecase import DeleteTenantRequestUsecase

# Real Estate Search
from modules.real_estate.infrastructure.repository.real_estate_repository import RealEstateRepository
from modules.tenant.application.usecase.get_recommend_list_usecase import GetRecommendListUsecase


def get_tenant_request_repository(db: Session = Depends(get_db_session)) -> TenantRequestRepository:
    """임차인 요청 Repository 의존성"""
    return TenantRequestRepository(db)


def get_create_tenant_request_usecase(
    repository: TenantRequestRepository = Depends(get_tenant_request_repository)
) -> CreateTenantRequestUsecase:
    """임차인 요청 생성 Usecase 의존성"""
    return CreateTenantRequestUsecase(repository)


def get_get_tenant_request_usecase(
    repository: TenantRequestRepository = Depends(get_tenant_request_repository)
) -> GetTenantRequestUsecase:
    """임차인 요청 조회 Usecase 의존성"""
    return GetTenantRequestUsecase(repository)


def get_update_tenant_request_usecase(
    repository: TenantRequestRepository = Depends(get_tenant_request_repository)
) -> UpdateTenantRequestUsecase:
    """임차인 요청 수정 Usecase 의존성"""
    return UpdateTenantRequestUsecase(repository)


def get_delete_tenant_request_usecase(
    repository: TenantRequestRepository = Depends(get_tenant_request_repository)
) -> DeleteTenantRequestUsecase:
    """임차인 요청 삭제 Usecase 의존성"""
    return DeleteTenantRequestUsecase(repository)


def get_real_estate_repository() -> RealEstateRepository:
    """부동산 매물 Repository 의존성"""
    return RealEstateRepository()


def get_recommend_list_usecase(
    repository: RealEstateRepository = Depends(get_real_estate_repository)
) -> GetRecommendListUsecase:
    """임차인 추천 매물 조회 Usecase 의존성"""
    return GetRecommendListUsecase(repository)
