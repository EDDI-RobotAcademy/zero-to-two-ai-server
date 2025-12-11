from pydantic import BaseModel


class TenantRecommendReasonInput(BaseModel):
    tenant_summary: str
    property_info: str


class TenantRecommendReasonOutput(BaseModel):
    reason: str