from __future__ import annotations

from typing import Dict, Optional

from modules.tenant.application.port.rental_request_repository import RentalRequestRepository
from modules.tenant.application.port.tenant_repository import TenantRepository
from modules.tenant.domain.rental_request import RentalRequest
from modules.tenant.domain.tenant import Tenant


class InMemoryTenantRepository(TenantRepository):
    def __init__(self) -> None:
        self._store: Dict[str, Tenant] = {}

    def get(self, tenant_id: str) -> Optional[Tenant]:
        return self._store.get(tenant_id)

    def save(self, tenant: Tenant) -> Tenant:
        self._store[tenant.id] = tenant
        return tenant


class InMemoryRentalRequestRepository(RentalRequestRepository):
    def __init__(self) -> None:
        self._store: Dict[str, RentalRequest] = {}

    def create(self, rental_request: RentalRequest) -> RentalRequest:
        self._store[rental_request.id] = rental_request
        return rental_request

    def update(self, rental_request: RentalRequest) -> RentalRequest:
        self._store[rental_request.id] = rental_request
        return rental_request