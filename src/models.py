from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TransactionType(Enum):
    RECEIVE = "RECEIVE"
    ISSUE = "ISSUE"


@dataclass
class Product:
    id: int
    name: str
    category: str
    quantity: int
    threshold: int
    unit_price: Optional[float] = None

    def __post_init__(self) -> None:
        if self.threshold < 0:
            raise ValueError("Threshold ต้องมากกว่าหรือเท่ากับ 0")
        if self.quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")


@dataclass
class StockTransaction:
    transaction_id: int
    product_id: int
    type: TransactionType
    quantity: int
    stock_before: int
    stock_after: int
    timestamp: datetime = field(default_factory=datetime.now)