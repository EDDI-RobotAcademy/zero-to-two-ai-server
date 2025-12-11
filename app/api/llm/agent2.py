from fastapi import APIRouter

from app.llm.schemas.agent2_schema import (
    TenantRecommendReasonInput,
    TenantRecommendReasonOutput,
)
from app.llm.services.agent2_service import generate_tenant_recommend_reason

router = APIRouter(prefix="/agent2", tags=["agent2"])


@router.post("/recommend/reason", response_model=TenantRecommendReasonOutput)
async def tenant_recommend_reason_endpoint(body: TenantRecommendReasonInput):
    return await generate_tenant_recommend_reason(body)