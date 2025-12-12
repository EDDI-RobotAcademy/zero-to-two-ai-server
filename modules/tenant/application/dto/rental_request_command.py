from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CreateRentalRequestCommand:
    tenant_id: str
    raw_requirements: str
    property_types: List[str]
    contract_type: str
    location_regions: List[str]
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None


@dataclass
class CreateRentalRequestResult:
    rental_request_id: str
    normalized_requirements: str
    tenant_id: str