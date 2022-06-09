# project imports;
import schemas, models, dependecies

# built-in imports;
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi import Response, status

def create_order(jwt: AuthJWT, order: schemas.OrderBase, db: Session):
    current_user_username = jwt.get_jwt_subject()
    user_qs = db.query(models.User).filter(models.User.username == current_user_username).first()
    order_db = models.Order(**order.dict(), user_id=user_qs.id)

    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

def update_order(id: int, jwt: AuthJWT, db: Session, order: schemas.OrderBase):

    order_qs = db.query(models.Order).filter(models.Order.id == id)
    order_qs.update(order.dict())
    db.commit()
    db.refresh(order_qs.first())

    return order_qs.first()

def update_order_status(id: int, order: schemas.OrderStatus, db: Session):

    order_qs = db.query(models.Order).filter(models.Order.id == id)
    order_qs.update({"order_status": order.order_status})
    db.commit()
    db.refresh(order_qs.first())

    return order_qs.first()
    
def delete_order(id: int, db: Session):

    order_qs = db.query(models.Order).filter(models.Order.id == id)
    order_qs.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_user_orders(jwt: AuthJWT, db: Session):
    current_user_username = jwt.get_jwt_subject()
    user_qs = db.query(models.User).filter(models.User.username == current_user_username).first()
    return db.query(models.Order).filter(models.Order.user_id == user_qs.id).all()

def get_all_orders(jwt: AuthJWT, db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, id: int):
    return dependecies.validate_order_id(id, db)