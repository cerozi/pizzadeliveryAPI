from fastapi import FastAPI
from routers.auth import auth_router
from routers.orders import order_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(order_router)
