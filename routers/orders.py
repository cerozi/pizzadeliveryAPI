from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from databases import get_db
from fastapi_jwt_auth import AuthJWT
import schemas
import dependecies
from repository import orders_crud
from decorators import staff_required

order_router = APIRouter(
    prefix = '/orders',
    tags = ['order']
)



@order_router.post('/order/', status_code=status.HTTP_201_CREATED)
def create_order(jwt: AuthJWT = Depends(dependecies.check_token), 
        order: schemas.OrderBase = Depends(dependecies.validate_order_data), 
         db: Session = Depends(get_db)):

    return orders_crud.create_order(jwt=jwt, order=order, db=db)

@order_router.put('/order/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_order(id: int, jwt: AuthJWT = Depends(dependecies.check_token), 
                db: Session = Depends(get_db), order: schemas.OrderBase = Depends(dependecies.check_order_owner)):

    return orders_crud.update_order(id=id, jwt=jwt, db=db, order=order)

@order_router.put('/order/update/status/{id}', status_code=status.HTTP_202_ACCEPTED)
@staff_required
def update_order_status(id: int, jwt: AuthJWT = Depends(dependecies.check_token), db: Session = Depends(get_db),
                        order_status: schemas.OrderStatus = Depends(dependecies.validate_order_status)):

    return orders_crud.update_order_status(id=id, order=order_status, db=db)

@order_router.delete('/order/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, jwt: AuthJWT = Depends(dependecies.check_token),
                db: Session = Depends(get_db), order: None = Depends(dependecies.check_order_owner)):
    
    return orders_crud.delete_order(id=id, db=db)