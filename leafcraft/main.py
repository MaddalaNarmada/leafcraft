from fastapi import FastAPI

from db.database import engine, Base
from models import models
from routers import products, orders, auth

app = FastAPI(
    title="Leafcraft E-Commerce API",
    description="""
    Leafcraft API for managing products and orders

    Features:
    Products - View and manage product inventory
    Orders - Create and manage customer orders
    Authentication - JWT-based secure authentication
    Caching - Redis caching for improved performance

    Authentication:
    Most order endpoints require JWT authentication. Use `/auth/login` to get your token.
    """
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

