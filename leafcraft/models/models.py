import enum
from sqlalchemy import Column, Integer, String, Float, JSON, Enum, DateTime, func

from db.database import Base


#creating table into database of named "Products"
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, nullable=False)
    created_ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


#Created Enum for representing order status of a order
class OrderStatus(str, enum.Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    cancelled = "Cancelled"


#creating table into database of named "Orders"
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    #below json storing list of product details
    items = Column(JSON, nullable=False)   #[{"product_id":2, "quantity":2}]
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)