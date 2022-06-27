from pydantic import BaseModel
from pydantic.class_validators import Optional


class UserCreateInput(BaseModel):
    name: str


class StandardOutput(BaseModel):
    message: str


class ErrorOutput(BaseModel):
    details: str


class UserListOutput(BaseModel):
    id: int
    name: str

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
