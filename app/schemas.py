# schemas.py
from typing import List, Optional
from pydantic import BaseModel

class CourierBase(BaseModel):
    name: str
    districts: List[str]

class CourierCreate(CourierBase):
    pass

class Courier(CourierBase):
    id: int
    active_order: Optional[dict] = None
    avg_order_complete_time: Optional[str] = None
    avg_day_orders: Optional[int] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    name: str
    district: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    courier_id: int
    status: int

    class Config:
        from_attributes = True