from fastapi import FastAPI
from routers.auth import auth_router
from routers.orders import order_router
from databases import Base, engine
from databases_test import test_engine
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=test_engine)

class Settings(BaseModel):
    authjwt_secret_key: str = 'a8a6ada27a3a06c8f2935bfe980e41806a5e16686a7db2159d2ccf967a0c9710'

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)
