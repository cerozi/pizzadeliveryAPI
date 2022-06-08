from fastapi import APIRouter

order_router = APIRouter(
    prefix = '/order',
    tags = ['order']
)



@order_router.get('/')
def index():
    return {"order_test": "test"}