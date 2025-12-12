from __future__ import annotations

from typing import Optional, Protocol

from modules.tenant.domain.tenant import Tenant


class TenantRepository(Protocol):
    def get(self, tenant_id: str) -> Optional[Tenant]:
        ...

    def save(self, tenant: Tenant) -> Tenant:
        ...