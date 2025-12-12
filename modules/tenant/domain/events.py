from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RentalRequestCreated:
    rental_request_id: str
    tenant_id: str
    created_at: datetime