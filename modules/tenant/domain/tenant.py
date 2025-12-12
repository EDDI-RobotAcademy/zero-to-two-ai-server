from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TenantRole(str, Enum):
    TENANT = "tenant"


@dataclass
class Tenant:
    id: str
    email: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    phone_visible: bool = False
    role: TenantRole = TenantRole.TENANT

    def allow_phone_sharing(self) -> None:
        self.phone_visible = True

    def hide_phone(self) -> None:
        self.phone_visible = False