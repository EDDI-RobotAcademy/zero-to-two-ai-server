from fastapi import APIRouter
from infrastructure.llm.client import ask_llm

router = APIRouter(prefix="/llm")

@router.post("/test")
def test_llm(query: dict):
    prompt = query.get("prompt")
    result = ask_llm(prompt)
    return {"response": result}