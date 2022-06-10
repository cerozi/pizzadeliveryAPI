# project imports;
import dependecies.orders_dependecies as orders_dependecies
import dependecies.auth_dependecies as auth_dependecies
import schemas
from databases import get_db
from decorators import staff_required
from repository import orders_crud

# built-in imports;
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

order_router = APIRouter(
    prefix = '/orders',
    tags = ['order']
)


# user creates an order;
@order_router.post('/order/', status_code=status.HTTP_201_CREATED)
def create_order(jwt: AuthJWT = Depends(auth_dependecies.check_token), 
        order: schemas.OrderBase = Depends(orders_dependecies.validate_order_data), 
         db: Session = Depends(get_db)):

    return orders_crud.create_order(jwt=jwt, order=order, db=db)

# user deletes an order;
@order_router.delete('/order/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, jwt: AuthJWT = Depends(auth_dependecies.check_token),
                db: Session = Depends(get_db), order: None = Depends(orders_dependecies.check_order_owner)):
    
    return orders_crud.delete_order(id=id, db=db)

# user updates an order;
@order_router.put('/order/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_order(id: int, jwt: AuthJWT = Depends(auth_dependecies.check_token), 
                db: Session = Depends(get_db), order: schemas.OrderBase = Depends(orders_dependecies.check_order_owner)):

    return orders_crud.update_order(id=id, jwt=jwt, db=db, order=order)

# user access all of his orders;
@order_router.get('/user/orders/', response_model=List[schemas.OrderRetrieve], status_code=status.HTTP_200_OK)
def get_user_orders(jwt: AuthJWT = Depends(auth_dependecies.check_token), db: Session = Depends(get_db)):
    return orders_crud.get_user_orders(jwt=jwt, db=db)


# user access a specific order;
@order_router.get('/user/orders/{id}', response_model=schemas.OrderRetrieve, status_code=status.HTTP_200_OK)
def get_order(id: int, jwt: AuthJWT = Depends(auth_dependecies.check_token), db: Session = Depends(get_db), order: None = Depends(orders_dependecies.check_order_owner)):
    return orders_crud.get_order(db=db, id=id)

# staffuser updates status of an order;
@order_router.put('/order/update/status/{id}', status_code=status.HTTP_202_ACCEPTED)
@staff_required
def update_order_status(id: int, jwt: AuthJWT = Depends(), db: Session = Depends(get_db),
                        order_status: schemas.OrderStatus = Depends(orders_dependecies.validate_order_status)):

    return orders_crud.update_order_status(id=id, order=order_status, db=db)


# staffuser get all orders from all users;
@order_router.get('/orders/', response_model=List[schemas.OrderRetrieve], status_code=status.HTTP_200_OK)
@staff_required
def get_all_orders(jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return orders_crud.get_all_orders(jwt=jwt, db=db)

# staffuser gets an specific order;
@order_router.get('/orders/{id}', response_model=schemas.OrderRetrieve, status_code=status.HTTP_200_OK)
@staff_required
def get_order(id: int, jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return orders_crud.get_order(db=db, id=id)
