from __future__ import annotations

from typing import Protocol

from modules.tenant.domain.rental_request import RentalRequest


class RentalRequestRepository(Protocol):
    def create(self, rental_request: RentalRequest) -> RentalRequest:
        ...

    def update(self, rental_request: RentalRequest) -> RentalRequest:
        ...