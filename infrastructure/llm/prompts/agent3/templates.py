from textwrap import dedent
from typing import List, Dict


def build_tenant_recommendations_prompt(
    listing_facts: List[str], tenant_profiles: List[Dict[str, str]],
) -> str:
    """
    Agent3: 임대인 매물 정보를 기반으로 적합한 임차인 후보를 추천하는 프롬프트.

    listing_facts 예시: ["마포구 공덕역 5분", "전세 5억", "84m²", "풀옵션"]
    tenant_profiles 예시: [{"id": "t-1", "nickname": "달리", "budget": "전세 5~6억", "preferred_area": "마포구", "house_type": "아파트"}]
    """

    facts = "\n".join(f"- {fact}" for fact in listing_facts)
    tenants = "\n".join(
        f"- id={t.get('id')} | {t.get('nickname')} | 예산={t.get('budget')} | 선호지역={t.get('preferred_area')} | 주거형태={t.get('house_type')} | 메모={t.get('notes', '')}"
        for t in tenant_profiles
    )

    return dedent(
        f"""
        너는 임대인 매물에 맞는 임차인 후보를 골라주는 에이전트다.
        - 예산/지역/주거형태/입주시기 등이 매물과 얼마나 맞는지 평가해 0~100점 매칭 점수를 계산한다.
        - 개인정보는 노출하지 말고, 입력에 없는 정보는 'unknown'으로 표시한다.
        - 부적합한 후보는 제외 사유를 red_flags로 적고 점수를 낮춰라.
        - JSON 스키마를 반드시 지키고, 자연어 설명을 추가하지 마라.

        [매물 핵심 정보]
        {facts}

        [임차인 후보]
        {tenants}

        [반환 JSON 스키마]
        {{
          "recommendations": [
            {{
              "tenant_id": "임차인 식별자",
              "match_score": 0-100,
              "fit_reasons": ["예산/지역/옵션 등 맞는 이유"],
              "missing_info": ["확인 필요 정보"],
              "red_flags": ["부적합 사유"]
            }}
          ],
          "style": "친절하지만 간결하게"
        }}
        """
    ).strip()


__all__ = ["build_tenant_recommendations_prompt"]