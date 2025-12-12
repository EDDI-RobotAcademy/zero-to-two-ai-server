import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gpt-4.1")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

async def ask_llm(prompt: str, top_k: int | None = None, tenant_request_id: int | None = None):
    """LLM 호출 (비동기). top_k/tenant_request_id는 현재 메시지에 포함만."""
    user_message = prompt
    if tenant_request_id is not None:
        user_message += f"\n\n[tenant_request_id: {tenant_request_id}]"
    if top_k is not None:
        user_message += f"\n\n[top_k: {top_k}]"

    if client is None:
        # 키가 없으면 모의 응답으로 동작 (개발용)
        return "LLM 키가 설정되지 않아 기본 안내를 제공합니다. 문의 내용을 남겨주시면 확인하겠습니다."

    def _call():
        return client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_message}],
        )

    response = await asyncio.to_thread(_call)
    return response.choices[0].message.content
