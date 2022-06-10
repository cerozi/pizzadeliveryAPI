from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False

class LoginSchema(BaseModel):
    username: str
    password: str

class OrderBase(BaseModel):
    quantity: int
    flavour: str
    size: str

    class Config:
        schema_extra = {
            'example': {
                    'quantity': 1,
                    'flavour': 'CHEESE',
                    'size': 'MEDIUM'
                }
            }

class OrderStatus(BaseModel):
    order_status: str

class FlavourBase(BaseModel):
    code: str
    value: str

    class Config:
        orm_mode = True

class SizeBase(FlavourBase):
    pass

class OrderStatusRetrieve(FlavourBase):
    pass

class OrderRetrieve(BaseModel):
    id: int
    quantity: int
    user_id: int
    order_status: OrderStatusRetrieve
    flavour: FlavourBase
    size: SizeBase

    class Config:
        orm_mode = True