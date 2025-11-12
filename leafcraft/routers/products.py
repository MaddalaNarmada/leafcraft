from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import Product
from schemas import schemas
from utils.cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/products", tags=["products"])


#creating new product into db
@router.post("/", response_model=schemas.ProductResponse, status_code=201, summary="Create new product")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    #added validations for quantity <0 and price <=0 and not accepting empty names and spaces
    if product.stock_quantity < 0:
        raise HTTPException(status_code=400, detail="Stock Quantity cannot be negative")
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")
    if product.name.strip() == '':
        raise HTTPException(status_code=400, detail="Product name cannot be empty")

    #added validation as product name should be unique
    product_name = db.query(Product).filter(Product.name == product.name).first()
    if product_name:
        raise HTTPException(status_code=400, detail="Product already exist")

    #validated all details and adding product into database
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)


    return db_product


#displaying list of all products with name, quantity and price
@router.get("/", response_model=list[schemas.ProductResponse], summary="Get all products")
def list_products(db:Session = Depends(get_db)):
    # Try cache first
    cached = get_cache("products_list")
    if cached:
        return cached

    # Cache miss - get from DB
    products = db.query(Product).all()
    products_dict = [{"id": p.id, "name": p.name, "stock_quantity": p.stock_quantity,
                      "price": p.price, "created_ts": p.created_ts, "updated_ts": p.updated_ts}
                     for p in products]

    # Store in cache
    set_cache("products_list", products_dict)
    return products_dict
