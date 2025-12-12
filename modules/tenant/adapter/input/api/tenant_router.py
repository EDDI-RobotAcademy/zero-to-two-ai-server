from __future__ import annotations

from typing import Callable

from modules.tenant.application.dto.rental_request_command import CreateRentalRequestCommand
from modules.tenant.application.usecase.create_rental_request import CreateRentalRequestUseCase


class TenantRouterStub:

    def __init__(self, create_rental_request_usecase: CreateRentalRequestUseCase) -> None:
        self._create_rental_request = create_rental_request_usecase

    def register(self, register_handler: Callable[..., None]) -> None:
        register_handler("POST", "/tenants/search", self.create_rental_request)

    def create_rental_request(self, payload: dict, tenant_id: str) -> dict:
        # 프론트 입력을 자연어로 변환 (Agent1 input)
        raw_text = f"""
        지역: {payload.get("region")}
        주거 형태: {payload.get("listingType")}
        계약 형태: {payload.get("contractType")}
        예산: {payload.get("budget")}만원
        최소 면적: {payload.get("areaMin")}㎡
        방 개수: {payload.get("rooms")}
        욕실 개수: {payload.get("bathrooms")}
        입주 가능 시기: {payload.get("moveInDate")}
        기타 요청사항: {payload.get("notes")}
        """

        command = CreateRentalRequestCommand(
            tenant_id=tenant_id,              # path param
            raw_requirements=raw_text,        # Agent1 핵심 입력
            expire_dt=None,                   # optional
        )

        result = self._create_rental_request.execute(command)
        return {
            "rental_request_id": result.rental_request_id,
            "normalized_requirements": result.normalized_requirements,
        }