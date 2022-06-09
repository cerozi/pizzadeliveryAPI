# project imports;
import dependecies.auth_dependecies as auth_dependecies
import schemas
from databases import get_db
from repository import auth_crud
# built-in projects;
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

# creates user;
@auth_router.post('/signup')
def index(request: schemas.UserBase = Depends(auth_dependecies.check_user), db: Session = Depends(get_db)):
    return auth_crud.creates_user(db=db, request=request)

# log user;
@auth_router.post('/login')
def user_login(request: schemas.LoginSchema, jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    data = auth_crud.user_login(jwt=jwt, db=db, request=request)
    if data:
        return data
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password invalid. ")

