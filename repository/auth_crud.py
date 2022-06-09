# project imports;
import models
import schemas
# built-in imports;
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash


def creates_user(db: Session, request: schemas.UserBase):
    user_db = models.User(**request.dict())
    user_db.password = generate_password_hash(request.password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

def user_login(jwt: AuthJWT, db: Session, request: schemas.LoginSchema):
    user_qs = db.query(models.User).filter(models.User.username==request.username).first()

    if not (user_qs and check_password_hash(user_qs.password, request.password)):
        return False

    access_token = jwt.create_access_token(subject=user_qs.username)
    refresh_token = jwt.create_refresh_token(subject=user_qs.username)

    data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return data
