from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from models import models
from db.database import get_db
from schemas import schemas
from utils.cache import get_cache, set_cache, delete_cache
from utils.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


#created helper function for calculating total value of an order
def total_value(db:Session, items):
    total = 0
    for item in items:
        #checking if quantity is not less than 0
        if item.quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity must be atleast 1")
        product = db.query(models.Product).get(item.product_id)
        #checking for product existence
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not exist")
        total += product.price * item.quantity
    return total

#creating new order and storing into db of authenticated user only
@router.post("/create_order", response_model=schemas.OrderResponse, summary="Create new order", status_code=201)
def create_order(order:schemas.OrderCreate, db:Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #checking if order contains atleast one item
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must need to have one item")

    #calling helper function to calculate total value
    total_amnt = total_value(db, order.items)

    #Validated details and adding record to db
    db_order_details = models.Order(items = [i.dict() for i in order.items], total_amount = total_amnt)
    db.add(db_order_details)
    db.commit()
    db.refresh(db_order_details)

    # Invalidate orders list cache
    delete_cache("orders_list")

    return db_order_details


#Confirming the order, updating order status, then updating stock quantity
@router.patch("/{order_id}/confirm", summary="Confirm order and update stock")
def confirm_order(order_id:int, db:Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    order = db.query(models.Order).get(order_id)
    if not order:
        raise HTTPException(status_code=400, detail=f"Order with {order_id} not found")

    #Making sure only order status with pending can be confirmed
    if order.status != models.OrderStatus.pending:
        raise HTTPException(status_code=400, detail="Only Orders with status can be confirmed")

    #checking stock before confirming order
    for item in order.items:
        product = db.query(models.Product).get(item['product_id'])
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not exist")
        if product.stock_quantity < item['quantity']:
            raise HTTPException(status_code=400, detail="Insufficient stock for one or more products")
        #if all good then reducing stock as order confirmed
        else:
            product.stock_quantity -= item['quantity']

    #updated stock and changed the status as confirmed
    order.status = models.OrderStatus.confirmed
    db.commit()

    # Invalidate both orders and products cache
    delete_cache("orders_list")
    delete_cache("products_list")

    return {"message": "Order Confirmed successfully"}

#Cacncelling the order, and restoring the stock
@router.patch("/{order_id}/cancel", summary="Cancel order and restore stock")
def cancel_order(order_id:int, db:Session=Depends(get_db), current_user: str = Depends(get_current_user)):
    order = db.query(models.Order).get(order_id)
    if not order:
        raise HTTPException(status_code=400, detail=f"Order with {order_id} not found")
    #Making sure if already cancelled orders will not be called again
    if order.status == models.OrderStatus.cancelled:
        raise HTTPException(status_code=400, detail="Orders cancelled already!")

    #Restoring stock if the order was confirmed
    if order.status == models.OrderStatus.confirmed:
        for item in order.items:
            product = db.query(models.Product).get(item['product_id'])
            #Adding quantity back
            product.stock_quantity += item['quantity']

    #Upadted quantity back and updating status
    order.status = models.OrderStatus.cancelled
    db.commit()

    # Invalidate both orders and products cache
    delete_cache("orders_list")
    delete_cache("products_list")

    return {"message":"Order cancelled"}

#list of all orders displaying with status of all
@router.get("/", response_model=list[schemas.OrderResponse], summary="Get all orders")
def list_oders(db:Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Try cache first
    cached = get_cache("orders_list")
    if cached:
        return cached

    # Cache miss - get from DB
    orders = db.query(models.Order).all()
    orders_dict = [{"id": o.id, "items": o.items, "total_amount": o.total_amount,
                    "status": o.status.value, "created_ts": o.created_ts, "updated_ts": o.updated_ts}
                   for o in orders]

    # Store in cache
    set_cache("orders_list", orders_dict)
    return orders_dict