from __future__ import annotations

from abc import ABC, abstractmethod

from modules.real_estate.application.dto.tenant_request_dto import (
    CreateTenantRequestCommand,
    CreateTenantRequestResult,
)


class CreateTenantRequestPort(ABC):
    @abstractmethod
    async def execute(self, cmd: CreateTenantRequestCommand) -> CreateTenantRequestResult:
        raise NotImplementedError
