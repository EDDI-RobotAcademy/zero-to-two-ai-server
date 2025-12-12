from typing import Optional

class RealEstate:
    def __init__(
        self,
        real_estate_id: int,
        title: str,
        area: float,
        room_count: int,
        bathroom_count: int,
        deal_type: str,
        cost: Optional[int],
        deposit: Optional[int],
        address: str,
        description: Optional[str],
    ):
        self.real_estate_id = real_estate_id
        self.title = title
        self.area = area
        self.room_count = room_count
        self.bathroom_count = bathroom_count
        self.deal_type = deal_type
        self.cost = cost
        self.deposit = deposit
        self.address = address
        self.description = description
