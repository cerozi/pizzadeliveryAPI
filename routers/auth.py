from fastapi import APIRouter, Depends, HTTPException, status
from databases import get_db
from sqlalchemy.orm import Session
import schemas, models
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

@auth_router.get('/test')
def test(jwt: AuthJWT = Depends()):
    try:
        jwt.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you must be logged to access this controller. ')

    current_user = jwt.get_jwt_subject()
    return {'logged_user': current_user}

@auth_router.post('/signup')
def index(request: schemas.UserBase, db: Session = Depends(get_db)):
    qs_username = db.query(models.User).filter(models.User.username == request.username).first()
    qs_email = db.query(models.User).filter(models.User.email == request.email).first()

    if qs_username or qs_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username or email already being used. ')

    user_db = models.User(**request.dict())
    user_db.password = generate_password_hash(request.password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@auth_router.post('/login')
def user_login(request: schemas.LoginSchema, jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user_qs = db.query(models.User).filter(models.User.username==request.username).first()

    if user_qs and check_password_hash(user_qs.password, request.password):
        access_token = jwt.create_access_token(subject=user_qs.username)
        refresh_token = jwt.create_refresh_token(subject=user_qs.username)

        data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return data

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='username or password invalid. ')