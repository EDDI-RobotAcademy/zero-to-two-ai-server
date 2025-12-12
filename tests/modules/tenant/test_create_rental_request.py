from modules.tenant.adapter.output.llm_requirement_normalizer_openai import (
    LLMRequirementNormalizerOpenAI,
)
from modules.tenant.adapter.output.recommendation_job_queue import (
    InMemoryRecommendationJobQueue,
)
from modules.tenant.adapter.output.repository_pg import (
    InMemoryRentalRequestRepository,
    InMemoryTenantRepository,
)
from modules.tenant.application.dto.rental_request_command import CreateRentalRequestCommand
from modules.tenant.application.usecase.create_rental_request import CreateRentalRequestUseCase
from modules.tenant.domain.tenant import Tenant


def test_create_rental_request_runs_end_to_end() -> None:
    tenant_repo = InMemoryTenantRepository()
    rental_request_repo = InMemoryRentalRequestRepository()
    llm_normalizer = LLMRequirementNormalizerOpenAI(llm_client=None)
    job_queue = InMemoryRecommendationJobQueue()

    tenant_repo.save(Tenant(id="tenant-1", email="user@example.com"))

    usecase = CreateRentalRequestUseCase(
        rental_request_repository=rental_request_repo,
        tenant_repository=tenant_repo,
        llm_requirement_normalizer=llm_normalizer,
        recommendation_job_queue=job_queue,
    )

    command = CreateRentalRequestCommand(
        tenant_id="tenant-1",
        raw_requirements="마포구 전세 원룸",
        property_types=["오피스텔"],
        contract_type="전세",
        location_regions=["마포구"],
        budget_min=100000,
        budget_max=200000,
    )

    result = usecase.execute(command)

    assert result.rental_request_id in rental_request_repo._store  # noqa: SLF001
    assert job_queue.enqueued[-1][0] == result.rental_request_id
    assert "normalized" in result.normalized_requirements