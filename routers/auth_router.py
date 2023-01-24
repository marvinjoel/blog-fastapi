from fastapi import APIRouter, status, HTTPException, Depends
from db.db_setup import SessionLocal, engine
from db.models import User
from routers.serializer import SignUpModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from routers.utils import validate_authorize

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = SessionLocal(bind=engine)


@auth_router.get('/')
async def blog_all(Authorize: AuthJWT = Depends()):
    validate_authorize(Authorize)
    return {"message": "is auth"}


# register
@auth_router.post('/signup', response_model=SignUpModel,status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with the email {db_email} already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_activate=user.is_activate,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return new_user


#login
@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.email)
        refresh_token = Authorize.create_refresh_token(subject=db_user.email)

        response = {
            "access": access_token,
            "refresh_token": refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid Email or Password')