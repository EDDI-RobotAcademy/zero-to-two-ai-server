from fastapi import APIRouter
from pydantic import BaseModel

class TenantSearchRequest(BaseModel):
    message: str

router = APIRouter(prefix="/tenant")

@router.post("/chatbot")
def search_by_message(request: TenantSearchRequest):
    result = ask_llm(request.message)
    return {"response": result}
