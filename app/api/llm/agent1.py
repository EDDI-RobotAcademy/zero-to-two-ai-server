from fastapi import APIRouter

from app.llm.schemas.agent1_schema import (
    PropertyDescriptionInput,
    PropertyDescriptionOutput,
    TenantRequirementInput,
    TenantRequirementOutput,
)
from app.llm.services.agent1_service import (
    clean_tenant_requirement,
    generate_property_description,
)

router = APIRouter(prefix="/agent1", tags=["agent1"])


@router.post("/tenant/clean", response_model=TenantRequirementOutput)
async def clean_tenant_requirement_endpoint(
    body: TenantRequirementInput,
):
    return await clean_tenant_requirement(body)


@router.post("/property/description", response_model=PropertyDescriptionOutput)
async def property_description_endpoint(
    body: PropertyDescriptionInput,
):
    return await generate_property_description(body)