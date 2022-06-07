from fastapi import APIRouter

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


@auth_router.get('/')
def index():
    return {"auth_test": "test"}