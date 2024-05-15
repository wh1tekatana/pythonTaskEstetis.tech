# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base

class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    districts = Column(ARRAY(String))
    active_order = Column(String, nullable=True)
    avg_order_complete_time = Column(String, nullable=True)
    avg_day_orders = Column(Integer, nullable=True)

    orders = relationship("Order", back_populates="courier")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district = Column(String, index=True)
    status = Column(Integer, default=1)  # 1 - in progress, 2 - completed
    courier_id = Column(Integer, ForeignKey("couriers.id"))

    courier = relationship("Courier", back_populates="orders")