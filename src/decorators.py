from functools import wraps
import models
from fastapi import HTTPException, status
from dependecies.auth_dependecies import check_token


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt = check_token(jwt=kwargs['jwt'])
        db = kwargs['db']

        current_user = jwt.get_jwt_subject()
        user_qs = db.query(models.User).filter(models.User.username == current_user).first()
        if user_qs.is_staff:
            return func(*args, **kwargs)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="only staff users can access this controller. ")

    return wrapper