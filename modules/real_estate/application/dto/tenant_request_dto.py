from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateTenantRequestCommand:
    user_id: int
    budget: Optional[int] = None
    preferred_area: Optional[str] = None
    family: Optional[str] = None
    age_range: Optional[str] = None
    job: Optional[str] = None
    commute_location: Optional[str] = None
    car_parking: Optional[bool] = None
    pet: Optional[bool] = None
    school_district: Optional[bool] = None
    lifestyle: Optional[str] = None
    expire_dt: Optional[str] = None  # ISO string expected


@dataclass
class CreateTenantRequestResult:
    tenant_request_id: int
    embedded: bool
