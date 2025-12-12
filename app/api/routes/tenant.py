from fastapi import APIRouter
from pydantic import BaseModel

from infrastructure.llm.client import ask_llm

class TenantSearchRequest(BaseModel):
    message: str
    tenant_request_id: int | None = None
    top_k: int | None = None

router = APIRouter(prefix="/tenant")

@router.post("/chatbot")
async def search_by_message(request: TenantSearchRequest):
    result = await ask_llm(
        request.message, top_k=request.top_k or 10, tenant_request_id=request.tenant_request_id
    )
    return {"response": result}
