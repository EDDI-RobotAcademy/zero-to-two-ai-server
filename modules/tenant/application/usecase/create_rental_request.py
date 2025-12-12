from __future__ import annotations

import uuid
from dataclasses import asdict
from datetime import datetime

from modules.tenant.application.dto.rental_request_command import (
    CreateRentalRequestCommand,
    CreateRentalRequestResult,
)
from modules.tenant.application.port.llm_requirement_normalizer import (
    LLMRequirementNormalizer,
)
from modules.tenant.application.port.recommendation_job_queue import RecommendationJobQueue
from modules.tenant.application.port.rental_request_repository import RentalRequestRepository
from modules.tenant.application.port.tenant_repository import TenantRepository
from modules.tenant.domain.events import RentalRequestCreated
from modules.tenant.domain.rental_request import Budget, LocationPreference, RentalRequest


class CreateRentalRequestUseCase:
    def __init__(
        self,
        rental_request_repository: RentalRequestRepository,
        tenant_repository: TenantRepository,
        llm_requirement_normalizer: LLMRequirementNormalizer,
        recommendation_job_queue: RecommendationJobQueue,
    ) -> None:
        self._rental_request_repository = rental_request_repository
        self._tenant_repository = tenant_repository
        self._llm_requirement_normalizer = llm_requirement_normalizer
        self._recommendation_job_queue = recommendation_job_queue

    def execute(self, command: CreateRentalRequestCommand) -> CreateRentalRequestResult:
        tenant = self._tenant_repository.get(command.tenant_id)
        if tenant is None:
            raise ValueError("Tenant not found")

        normalized = self._llm_requirement_normalizer.normalize(
            raw_requirements=command.raw_requirements,
            location_regions=command.location_regions,
            property_types=command.property_types,
        )

        rental_request = RentalRequest(
            id=str(uuid.uuid4()),
            tenant_id=command.tenant_id,
            property_types=command.property_types,
            contract_type=command.contract_type,
            requirements_text=normalized,
            location_preference=LocationPreference(regions=command.location_regions),
            budget=Budget(minimum=command.budget_min, maximum=command.budget_max),
        )

        persisted = self._rental_request_repository.create(rental_request)

        event = RentalRequestCreated(
            rental_request_id=persisted.id,
            tenant_id=persisted.tenant_id,
            created_at=datetime.utcnow(),
        )
        self._publish(event)

        self._recommendation_job_queue.enqueue(persisted.id, persisted.tenant_id)

        return CreateRentalRequestResult(
            rental_request_id=persisted.id,
            normalized_requirements=normalized,
            tenant_id=persisted.tenant_id,
        )

    def _publish(self, event: RentalRequestCreated) -> None:
        # Placeholder for a future domain event dispatcher
        _ = asdict(event)