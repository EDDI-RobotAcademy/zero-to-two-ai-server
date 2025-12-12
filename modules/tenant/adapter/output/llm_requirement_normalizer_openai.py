from __future__ import annotations

from typing import List

from modules.tenant.application.port.llm_requirement_normalizer import LLMRequirementNormalizer


class LLMRequirementNormalizerOpenAI(LLMRequirementNormalizer):
    def __init__(self, llm_client: object) -> None:
        self._llm_client = llm_client

    def normalize(
        self, *, raw_requirements: str, location_regions: List[str], property_types: List[str]
    ) -> str:
        context = {
            "raw": raw_requirements,
            "regions": ", ".join(location_regions),
            "types": ", ".join(property_types),
        }
        return f"[normalized] {context['raw']} ({context['regions']}; {context['types']})"