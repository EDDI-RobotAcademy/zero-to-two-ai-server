"""
Tenant Request Router
임차인 요청 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from modules.tenant.application.dto.tenant_recommended_real_estate_dto import TenantRecommendedRealEstateDTO
from modules.tenant.application.dto.tenant_request_dto import (
    TenantRequestCreateDTO,
    TenantRequestUpdateDTO,
    TenantRequestIdResponseDTO,
    TenantRequestSummaryDTO,
    TenantRequestResponseDTO
)
from modules.tenant.application.dto.tenant_request_recommend_dto import TenantRequestRecommendDTO
from modules.tenant.application.usecase.create_tenant_request_usecase import CreateTenantRequestUsecase
from modules.tenant.application.usecase.get_recommend_list_usecase import GetRecommendListUsecase
from modules.tenant.application.usecase.get_tenant_request_usecase import GetTenantRequestUsecase
from modules.tenant.application.usecase.update_tenant_request_usecase import UpdateTenantRequestUsecase
from modules.tenant.application.usecase.delete_tenant_request_usecase import DeleteTenantRequestUsecase
from modules.tenant.adapter.input.web.dependencies import (
    get_create_tenant_request_usecase,
    get_get_tenant_request_usecase,
    get_update_tenant_request_usecase,
    get_delete_tenant_request_usecase,
    get_recommend_list_usecase
)
from modules.auth.adapter.input.auth_middleware import auth_required

router = APIRouter(prefix="/tenant", tags=["Tenant Requests"])


@router.post("/request", response_model=TenantRequestIdResponseDTO, status_code=status.HTTP_201_CREATED)
def create_tenant_request(
    dto: TenantRequestCreateDTO,
    user_id: int = Depends(auth_required),
    usecase: CreateTenantRequestUsecase = Depends(get_create_tenant_request_usecase)
):
    """
    임차인 요청 생성

    인증된 사용자가 새로운 매물 요청을 생성합니다.
    """
    try:
        result = usecase.execute(user_id, dto)
        return TenantRequestIdResponseDTO(tenant_request_id=result.tenant_request_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/request", response_model=List[TenantRequestSummaryDTO])
def get_my_tenant_requests(
    user_id: int = Depends(auth_required),
    usecase: GetTenantRequestUsecase = Depends(get_get_tenant_request_usecase)
):
    """
    내 임차인 요청 목록 조회

    인증된 사용자가 자신이 작성한 모든 임차인 요청을 조회합니다.
    """
    try:
        results = usecase.execute_by_user(user_id)
        return [
            TenantRequestSummaryDTO(
                tenant_request_id=r.tenant_request_id,
                preferred_area=r.preferred_area,
                residence_type=r.residence_type,
                deal_type=r.deal_type,
                budget=r.budget
            ) for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/request/{id}", response_model=TenantRequestResponseDTO)
def get_tenant_request(
    id: int,
    user_id: int = Depends(auth_required),
    usecase: GetTenantRequestUsecase = Depends(get_get_tenant_request_usecase)
):
    """
    임차인 요청 단건 조회

    특정 ID의 임차인 요청을 조회합니다. (본인 소유만 가능)
    """
    try:
        result = usecase.execute_by_id(id, user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"임차인 요청을 찾을 수 없습니다: {id}"
            )
        return result
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/request/{id}", response_model=TenantRequestIdResponseDTO)
def update_tenant_request(
    id: int,
    dto: TenantRequestUpdateDTO,
    user_id: int = Depends(auth_required),
    usecase: UpdateTenantRequestUsecase = Depends(get_update_tenant_request_usecase)
):
    """
    임차인 요청 수정

    특정 ID의 임차인 요청을 수정합니다. (본인 소유만 가능)
    """
    try:
        result = usecase.execute(id, user_id, dto)
        return TenantRequestIdResponseDTO(tenant_request_id=result.tenant_request_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/request/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant_request(
    id: int,
    user_id: int = Depends(auth_required),
    usecase: DeleteTenantRequestUsecase = Depends(get_delete_tenant_request_usecase)
):
    """
    임차인 요청 삭제

    특정 ID의 임차인 요청을 삭제합니다. (본인 소유만 가능)
    """
    try:
        success = usecase.execute(id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"임차인 요청을 찾을 수 없습니다: {id}"
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/recommendations",
    response_model=List[TenantRecommendedRealEstateDTO],
)
def recommend_real_estates(
    dto: TenantRequestRecommendDTO,
    user_id: int = Depends(auth_required),
    usecase: GetRecommendListUsecase = Depends(get_recommend_list_usecase),
):
    return usecase.execute(dto, user_id)