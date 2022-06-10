# built-in imports;
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# project imports;
import schemas, models
from databases import get_db


# checks if user is logged;
def check_token(jwt: AuthJWT = Depends()):
    try:
        jwt.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="only logged users can access this controller. ")

    return jwt

# checks if user already exists;
def check_user(request: schemas.UserBase, db: Session = Depends(get_db)):
    qs_username = db.query(models.User).filter(models.User.username == request.username).first()
    qs_email = db.query(models.User).filter(models.User.email == request.email).first()

    if qs_username or qs_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username or email already being used. ')

    return request
