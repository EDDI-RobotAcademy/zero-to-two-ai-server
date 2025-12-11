from pydantic import BaseModel


class TenantRequirementInput(BaseModel):
    tenant_raw_input: str


class TenantRequirementOutput(BaseModel):
    clean_summary: str


class PropertyDescriptionInput(BaseModel):
    property_raw_input: str


class PropertyDescriptionOutput(BaseModel):
    description: str