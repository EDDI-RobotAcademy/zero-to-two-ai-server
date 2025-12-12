from __future__ import annotations

from typing import List, Protocol


class LLMRequirementNormalizer(Protocol):
    def normalize(self, *, raw_requirements: str, location_regions: List[str], property_types: List[str]) -> str:
        ...