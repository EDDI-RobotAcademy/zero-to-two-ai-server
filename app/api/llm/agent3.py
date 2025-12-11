from fastapi import APIRouter

from app.llm.schemas.agent3_schema import (
    LandlordRecommendReasonInput,
    LandlordRecommendReasonOutput,
)
from app.llm.services.agent3_service import generate_landlord_recommend_reason

router = APIRouter(prefix="/agent3", tags=["agent3"])


@router.post("/recommend/reason", response_model=LandlordRecommendReasonOutput)
async def landlord_recommend_reason_endpoint(
    body: LandlordRecommendReasonInput,
):
    return await generate_landlord_recommend_reason(body)