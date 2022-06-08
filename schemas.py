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