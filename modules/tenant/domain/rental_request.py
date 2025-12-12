from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class LocationPreference:
    regions: List[str] = field(default_factory=list)


@dataclass
class Budget:
    minimum: Optional[int] = None
    maximum: Optional[int] = None

    def is_within(self, amount: int) -> bool:
        lower_ok = self.minimum is None or amount >= self.minimum
        upper_ok = self.maximum is None or amount <= self.maximum
        return lower_ok and upper_ok


@dataclass
class RentalRequest:
    id: str
    tenant_id: str
    property_types: List[str]
    contract_type: str
    requirements_text: str
    location_preference: LocationPreference = field(default_factory=LocationPreference)
    budget: Budget = field(default_factory=Budget)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update_requirements(self, requirements_text: str) -> None:
        self.requirements_text = requirements_text
        self.updated_at = datetime.utcnow()

    def update_budget(self, minimum: Optional[int], maximum: Optional[int]) -> None:
        self.budget.minimum = minimum
        self.budget.maximum = maximum
        self.updated_at = datetime.utcnow()

    def update_location(self, regions: List[str]) -> None:
        self.location_preference.regions = regions
        self.updated_at = datetime.utcnow()