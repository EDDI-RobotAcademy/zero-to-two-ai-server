from __future__ import annotations

from typing import Callable

from modules.tenant.application.dto.rental_request_command import CreateRentalRequestCommand
from modules.tenant.application.usecase.create_rental_request import CreateRentalRequestUseCase


class TenantRouterStub:
    """
    Placeholder for a web framework router.
    Wire this to FastAPI/Starlette in `app/api/routers/tenant.py`.
    """

    def __init__(self, create_rental_request_usecase: CreateRentalRequestUseCase) -> None:
        self._create_rental_request = create_rental_request_usecase

    def register(self, register_handler: Callable[..., None]) -> None:
        register_handler("POST", "/tenants/{tenant_id}/rental-requests", self.create_rental_request)

    def create_rental_request(self, payload: dict, tenant_id: str) -> dict:
        command = CreateRentalRequestCommand(
            tenant_id=tenant_id,
            raw_requirements=payload.get("requirements", ""),
            property_types=payload.get("property_types", []),
            contract_type=payload.get("contract_type", ""),
            location_regions=payload.get("location_regions", []),
            budget_min=payload.get("budget_min"),
            budget_max=payload.get("budget_max"),
        )
        result = self._create_rental_request.execute(command)
        return {
            "rental_request_id": result.rental_request_id,
            "normalized_requirements": result.normalized_requirements,
        }