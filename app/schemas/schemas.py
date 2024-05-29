from pydantic import UUID4, BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserLogin(UserCreate):
    pass


class JWTTokenDTO(BaseModel):
    access_token: str


class User(BaseModel):
    id: UUID4
    email: EmailStr

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    text: constr(max_length=1048576)


class PostCreatedDTO(BaseModel):
    id: UUID4


class Post(BaseModel):
    id: UUID4
    text: str
    owner_id: UUID4

    class Config:
        from_attributes = True


class PostsDTO(BaseModel):
    posts: list[Post]

    class Config:
        from_attributes = True


