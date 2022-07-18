from pydantic import BaseModel
from pydantic.class_validators import Optional

class TokenSchema(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]

    class Config:
        orm_mode = True


class UserCreateInput(BaseModel):
    email: Optional[str]
    password: Optional[str]

class UserOut(BaseModel):
    id: Optional[int]
    name: Optional[str]
    user_type: Optional[int]
    email:  Optional[str]

    class Config:
        orm_mode = True

class UserCreate(UserOut):
    id: Optional[int]
    name: Optional[str]
    email: Optional[int]

class StandardOutput(BaseModel):
    message: str


class ErrorOutput(BaseModel):
    details: str


class UserListOutput(BaseModel):
    id: int
    email: str


    class Config:
        orm_mode = True


class AuthorCreateInput(BaseModel):
    name: Optional[str]
    picture: Optional[str]

    class Config:
        orm_mode = True


class AuthorUpdateInput(BaseModel):
    name: str
    picture: str

class AuthorPrintInput(BaseModel):
    id : Optional[int]
    name: Optional[str]
    picture: Optional[str]

    class Config:
        orm_mode = True




class PaperCreateInput(BaseModel):
    category: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    firstParagraph: Optional[str]
    body: Optional[str]
    author_id: Optional[int]
    class Config:
        orm_mode = True


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class SystemUser (BaseModel):
    password: str


# Optional , e pq o pydentc solta uma exceção quando recebe null no campo
class AuthorlistOutput(BaseModel):
    id: int
    name: Optional[str]
    picture: Optional[str]
    category: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    class Config:
        orm_mode = True


class PaperOutput(BaseModel):
    id: int
    category: str
    title: str
    summary: str
    firstParagraph: str
    body: str

    class Config:
        orm_mode = True
