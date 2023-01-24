from pydantic import BaseModel, EmailStr
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool]
    is_activate: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'username': 'mario',
                'email': 'mario@gmail.com',
                'password': 'password',
                'is_staff': False,
                'is_activate': True,
            }
        }


# token JWT
class Settings(BaseModel):
    authjwt_secret_key: str = 'b2070c27d807a0b0bf7e9f568c0af639c881a238b74bd15d306b765841713929'


class LoginModel(BaseModel):
    email: EmailStr
    password: str


#blogs
class BlogModel(BaseModel):
    id: Optional[int]
    title: str
    body: str
    type_b: Optional[str] = "FREE-TOPIC"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Clean Code",
                "body": "Welcome book",
                "type_b": "FREE-TOPIC"
            }
        }