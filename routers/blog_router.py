from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from db.db_setup import SessionLocal, engine
from db.models import User, Blog
# from routers.serializer import BlogModel
from routers.serializer import BlogModel
from routers.utils import validate_authorize

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)

session = SessionLocal(bind=engine)


@blog_router.get('/')
async def blog_all():
    blogs = session.query(Blog).all()
    return jsonable_encoder(blogs)


@blog_router.post('/blog', status_code=status.HTTP_201_CREATED)
async def add_blog(blog: BlogModel, Authorize: AuthJWT = Depends()):
    validate_authorize(Authorize)

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == current_user).first()

    new_blog = Blog(
        title=blog.title,
        body=blog.body,
        type_b=blog.type_b
    )

    new_blog.user = user
    session.add(new_blog)
    session.commit()

    response = {
        "title": new_blog.title,
        "body": new_blog.body,
        "type_b": new_blog.type_b,
        "id": new_blog.id
    }

    return jsonable_encoder(response)