from fastapi import APIRouter
from pydantic import BaseModel

from infrastructure.llm.client import ask_llm

class TenantSearchRequest(BaseModel):
    message: str


router = APIRouter(prefix="/tenant")


@router.post("/chatbot")
def search_by_message(request: TenantSearchRequest):
    result = ask_llm(request.message)
    return {"response": result}
