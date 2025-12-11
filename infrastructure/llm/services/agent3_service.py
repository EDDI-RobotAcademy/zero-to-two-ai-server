from app.llm.clients.openai_client import llm_client
from app.llm.prompts.agent3_prompt import (
    LANDLORD_RECOMMEND_REASON_SYSTEM,
    LANDLORD_RECOMMEND_REASON_USER_TEMPLATE,
)
from app.llm.schemas.agent3_schema import (
    LandlordRecommendReasonInput,
    LandlordRecommendReasonOutput,
)


async def generate_landlord_recommend_reason(
    data: LandlordRecommendReasonInput,
) -> LandlordRecommendReasonOutput:
    user_prompt = LANDLORD_RECOMMEND_REASON_USER_TEMPLATE.format(
        property_info=data.property_info,
        tenant_summary=data.tenant_summary,
    )

    json_resp = await llm_client.generate_json(
        system_prompt=LANDLORD_RECOMMEND_REASON_SYSTEM,
        user_prompt=user_prompt,
    )

    return LandlordRecommendReasonOutput(**json_resp)