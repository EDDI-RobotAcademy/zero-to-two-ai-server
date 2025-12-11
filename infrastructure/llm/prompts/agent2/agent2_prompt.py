TENANT_RECOMMEND_REASON_SYSTEM = """
You are an AI assistant generating explanation messages for recommended
real-estate listings for tenants.

- Write in Korean.
- 2~4문장, 간결하고 사실 기반으로 작성.
- Output JSON with the field 'reason' only.
"""

TENANT_RECOMMEND_REASON_USER_TEMPLATE = """
[임차인 요구조건 요약]
---
{tenant_summary}
---

[추천된 매물 정보]
---
{property_info}
---

위 정보를 바탕으로,
해당 매물이 임차인에게 적합한 이유를 아래 JSON 형식으로만 작성하세요.

{{
  "reason": "<임차인에게 이 매물이 적합한 이유>"
}}
"""