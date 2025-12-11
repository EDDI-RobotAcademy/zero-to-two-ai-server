from textwrap import dedent
from typing import List, Dict


def build_listing_recommendations_prompt(
    requirement_summary: Dict[str, List[str]], candidate_listings: List[Dict[str, str]]
) -> str:
    """
    Agent2: 임차인 요구조건을 기반으로 매물 추천을 설명하는 프롬프트.

    requirement_summary 예시:
    {"must_conditions": ["마포구"], "nice_to_have": ["풀옵션"], "style": "친절"}
    candidate_listings 예시:
    [{"id": "apt-1", "title": "마포역 초역세권", "location": "마포구", "price": "전세 5억", "size": "84m²", "features": "풀옵션, 남향"}]
    """

    must = "\n".join(f"- {item}" for item in requirement_summary.get("must_conditions", []))
    nice = "\n".join(f"- {item}" for item in requirement_summary.get("nice_to_have", []))
    listings = "\n".join(
        f"- id={c.get('id')} | {c.get('title')} | {c.get('location')} | {c.get('price')} | {c.get('size')} | {c.get('features')}"
        for c in candidate_listings
    )
    tone = requirement_summary.get("style", "친절하고 간결하게")

    return dedent(
        f"""
        너는 임차인 요구조건을 보고 가장 적합한 매물을 골라주는 에이전트다.
        - 필수 조건을 만족하는 매물만 추천하고, 그렇지 않으면 제외 사유를 적어라.
        - 가격·위치·평형·옵션을 기준으로 0~100점 매칭 점수를 계산한다.
        - 근거를 bullet로 제시하고, 누락된 정보나 주의사항도 함께 명시한다.
        - JSON 스키마를 엄격히 지키고, 불필요한 설명은 넣지 말라.

        [필수 조건]
        {must}

        [있으면 좋은 조건]
        {nice if nice else '- (없음)'}

        [후보 매물]
        {listings}

        [반환 JSON 스키마]
        {{
          "recommendations": [
            {{
              "listing_id": "매물 식별자",
              "match_score": 0-100,
              "reasons": ["선정 근거"],
              "missing_info": ["알 수 없어서 감점한 항목"],
              "red_flags": ["주의해야 할 점"]
            }}
          ],
          "style": "{tone}"
        }}
        """
    ).strip()


__all__ = ["build_listing_recommendations_prompt"]