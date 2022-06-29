from pydantic import BaseModel
from pydantic.class_validators import Optional


class UserCreateInput(BaseModel):
    email: Optional[str]
    password: Optional[str]

class UserOut(BaseModel):
    id : Optional[int]
    name: Optional[str]
    user_type: Optional[str]
    email:  Optional[int]

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
    name: str
    picture: str


class AuthorUpdateInput(BaseModel):
    name: str
    picture: str


class PaperCreateInput(BaseModel):
    category: str
    title: str
    summary: str
    firstParagraph: str
    body: str


# Optional , e pq o pydentc solta uma exceção quando recebe null no campo
class AuthorlistOutput(BaseModel):
    id: int
    name: Optional[str]
    picture: Optional[str]

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
