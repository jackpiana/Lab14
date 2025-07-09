from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen= True, order= True)
class Order:
    order_id: int
    customer_id: int
    order_status: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    store_id: int
    staff_id: int

    def __repr__(self):
        return f"ordine nr.: {self.order_id}"
