from fastapi import FastAPI
from routers import auth_router, blog_router
from fastapi_jwt_auth import AuthJWT
from routers.serializer import Settings

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router.auth_router)
app.include_router(blog_router.blog_router)