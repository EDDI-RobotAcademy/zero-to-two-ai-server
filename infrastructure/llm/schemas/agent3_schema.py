from pydantic import BaseModel


class LandlordRecommendReasonInput(BaseModel):
    property_info: str
    tenant_summary: str


class LandlordRecommendReasonOutput(BaseModel):
    reason: str