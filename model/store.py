from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Store:
    store_id: int
    store_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: int

    def __str__(self):
        return f"store {self.store_name}"
