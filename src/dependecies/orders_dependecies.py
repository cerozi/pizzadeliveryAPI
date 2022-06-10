# built-in imports;
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# project imports;
import schemas, models
from databases import get_db


# checks if the order has a valid id;
def validate_order_id(id: int, db: Session):
    order_qs = db.query(models.Order).filter(models.Order.id == id).first()
    if not order_qs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this order doesn't exist. ")
    
    return order_qs

# checks the request body from the order
def validate_order_data(order: schemas.OrderBase | None = None):
    '''
        if the request body has unvalid values for flavour or size, raises an exception
    '''

    if not (order == None):
        from models import Order
        flavour_list = [flavour[0] for flavour in Order.FLAVOURS_CHOICES]
        size_list = [size[0] for size in Order.SIZES_CHOICES]
        if order.flavour not in flavour_list or order.size not in size_list:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid request data body. ")
    
    return order

# checks the request body from the order
def validate_order_status(id: int, order: schemas.OrderStatus, db: Session = Depends(get_db)):
    validate_order_id(id=id, db=db)

    '''
        if the request body has unvalid values status, raises an exception
    '''

    from models import Order
    order_status = [order_choice[0] for order_choice in Order.ORDER_STATUS]
    if order.order_status not in order_status:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid request body. ")
    
    return order

# validates if the request user owns the order that he is trying to access;
def check_order_owner(id: int, jwt: AuthJWT = Depends(), db: Session = Depends(get_db), 
                            order: schemas.OrderBase | None = Depends(validate_order_data)):

    order_qs = validate_order_id(id=id, db=db)

    current_user_username = jwt.get_jwt_subject()
    user_qs = db.query(models.User).filter(models.User.username == current_user_username).first()
    if order_qs.user_id != user_qs.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can't access this order. ")

    return order

