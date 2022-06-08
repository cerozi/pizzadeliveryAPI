from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False

class LoginSchema(BaseModel):
    username: str
    password: str