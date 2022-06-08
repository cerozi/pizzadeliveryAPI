from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models
from databases import get_db

def check_token(jwt: AuthJWT = Depends()):
    try:
        jwt.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="only logged users can access this controller. ")

    return jwt

def validate_order_id(id: int, db: Session):
    order_qs = db.query(models.Order).filter(models.Order.id == id).first()
    if not order_qs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this order doesn't exist. ")
    
    return order_qs

def validate_order_data(order: schemas.OrderBase | None = None):
    if not (order == None):
        from models import Order
        flavour_list = [flavour[0] for flavour in Order.FLAVOURS_CHOICES]
        size_list = [size[0] for size in Order.SIZES_CHOICES]
        if order.flavour not in flavour_list or order.size not in size_list:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid request data body. ")
    
    return order


def validate_order_status(id: int, order: schemas.OrderStatus, db: Session = Depends(get_db)):
    validate_order_id(id=id, db=db)

    from models import Order
    order_status = [order_choice[0] for order_choice in Order.ORDER_STATUS]
    if order.order_status not in order_status:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid request body. ")
    
    return order


def check_order_owner(id: int, jwt: AuthJWT = Depends(), db: Session = Depends(get_db), 
                            order: schemas.OrderBase | None = Depends(validate_order_data)):

    order_qs = validate_order_id(id=id, db=db)

    current_user_username = jwt.get_jwt_subject()
    user_qs = db.query(models.User).filter(models.User.username == current_user_username).first()
    if order_qs.user_id != user_qs.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can't access this order. ")

    return order

