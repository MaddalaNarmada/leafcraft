from typing import List
from pydantic import BaseModel, Field

# schema for crreating new product
class ProductCreate(BaseModel):
    #validates data from api requests before saving into db
    name: str = Field(..., description="Product name", example="Green Tea Premium")
    stock_quantity: int = Field(..., description="Available stock quantity", example=10)
    price: float = Field(..., description="Product price in USD", example=25.99)

#schema for returning product details in API responses
#extends product create
class ProductResponse(ProductCreate):
    id: int = Field(..., description="Product unique identifier", example=1)
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Green Tea Premium",
                "stock_quantity": 100,
                "price": 25.99
            }
        }

# schema for creating a single item in an order
class OrderItem(BaseModel):
    product_id: int = Field(..., description="Product ID to order", example=1)
    quantity: int = Field(..., description="Quantity to order", example=2, gt=0)


#schema for creating new order with list of items
class OrderCreate(BaseModel):
    items: List[OrderItem] = Field(..., description="List of items to order")

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ]
            }
        }

#schema for returning order details in API response
class OrderResponse(BaseModel):
    id: int = Field(..., description="Order unique identifier")
    items: List = Field(..., description="List of ordered items")
    total_amount: float = Field(..., description="Total order amount in USD")
    status: str = Field(..., description="Order status: Pending, Confirmed, or Cancelled")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ],
                "total_amount": 75.50,
                "status": "Pending"
            }
        }
        
