from app.llm.clients.openai_client import llm_client
from app.llm.prompts.agent1_prompt import (
    PROPERTY_DESCRIPTION_SYSTEM,
    PROPERTY_DESCRIPTION_USER_TEMPLATE,
    TENANT_REQUIREMENT_SYSTEM,
    TENANT_REQUIREMENT_USER_TEMPLATE,
)
from app.llm.schemas.agent1_schema import (
    PropertyDescriptionInput,
    PropertyDescriptionOutput,
    TenantRequirementInput,
    TenantRequirementOutput,
)


async def clean_tenant_requirement(
    data: TenantRequirementInput,
) -> TenantRequirementOutput:
    user_prompt = TENANT_REQUIREMENT_USER_TEMPLATE.format(
        tenant_raw_input=data.tenant_raw_input
    )

    json_resp = await llm_client.generate_json(
        system_prompt=TENANT_REQUIREMENT_SYSTEM,
        user_prompt=user_prompt,
    )

    return TenantRequirementOutput(**json_resp)


async def generate_property_description(
    data: PropertyDescriptionInput,
) -> PropertyDescriptionOutput:
    user_prompt = PROPERTY_DESCRIPTION_USER_TEMPLATE.format(
        property_raw_input=data.property_raw_input
    )

    json_resp = await llm_client.generate_json(
        system_prompt=PROPERTY_DESCRIPTION_SYSTEM,
        user_prompt=user_prompt,
    )

    return PropertyDescriptionOutput(**json_resp)