from schemas import  TokenSchema
from auth.auth import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.class_validators import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, get_hashed_password, get_current_user
from database.models import Author, User, Papers
from services import UserService, AuthorService, PaperService
from schemas import UserCreateInput, StandardOutput, UserListOutput, AuthorCreateInput, AuthorlistOutput, \
    PaperCreateInput, AuthorUpdateInput, PaperOutput, UserOut, UserCreate, AuthorPrintInput
import logging

user_router = APIRouter(prefix='/user')
author_router = APIRouter(prefix='/authors')
papers_router = APIRouter(prefix='/papers')
auth_router = APIRouter(prefix='/auth')


@user_router.post('/signup', summary="Create new user", response_model=UserListOutput)
async def create_user(data: UserCreateInput, db: AsyncSession = Depends(get_session)):
    # querying database to check if user already exist
    async with db as session:
        query = select(User).filter(User.email == data.email)
        result = await session.execute(query)
        user_create = result.scalars().first()
        if user_create is None:
            user = {
                'email': data.email,
                'password': get_hashed_password(data.password)

            }
            db.add(User(email=user['email'], password=user['password']))
            await db.commit()
            query2 = select(User.id).filter(User.email == data.email)
            result = await session.execute(query2)
            id_current_user = result.scalar_one_or_none()
            UserListOutput.id = id_current_user
            UserListOutput.email = user['email']
            return UserListOutput
        else:
            raise HTTPException(detail='Email is in use', status_code=status.HTTP_404_NOT_FOUND)

    return


@user_router.get('/', response_model=List[UserOut])
async def get_user(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(User)
        result = await session.execute(query)
        user_list: List[User] = result.scalars().all()

        return user_list


@user_router.delete('/delete/{user_id}', summary="Delete user", response_model=StandardOutput)
async def user_create(user_id: int):
    try:
        await UserService.delete_user(user_id)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@author_router.post('/REGISTRATION/', status_code=status.HTTP_201_CREATED, response_model=AuthorPrintInput)

async def author_create(author_input: AuthorPrintInput, db: AsyncSession = Depends(get_session)):
    new_author = Author(name=author_input.name, picture=author_input.picture)
    db.add(new_author)
    await db.commit()

    return new_author

@author_router.put('/UPDATE/{author_id}')
async def up_author(author_id: int, author_input: AuthorUpdateInput, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Author).filter(Author.id == author_id)
        result = await session.execute(query)
        author_update = result.scalar_one_or_none()
        if author_update:
            author_update.name = author_input.name
            author_update.picture = author_input.picture
            await session.commit()
            return author_update
        else:
            raise HTTPException(detail='Author not found', status_code=status.HTTP_404_NOT_FOUND)

@author_router.get('/', response_model=List[AuthorlistOutput])
async def get_me(user: User = Depends(get_current_user)):
    return user
async def author_list():
    try:
        return await AuthorService.list_author()
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))





@author_router.get('/{name}', response_model=List[AuthorlistOutput])
async def author_list(name):
    try:
        return await AuthorService.search_author(name)
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@papers_router.post('/REGISTRATION/', status_code=status.HTTP_201_CREATED, response_model=PaperCreateInput)
async def author_create(paper_input: PaperCreateInput, db: AsyncSession = Depends(get_session)):
    new_paper = Papers(category=paper_input.category, title=paper_input.title, summary=paper_input.summary,
                    firstParagraph=paper_input.firstParagraph, body=paper_input.body, author_id=paper_input.author_id)
    db.add(new_paper)
    await db.commit()

    return new_paper


@papers_router.put('/UPDATE/{paper_id}')
async def up_paper(paper_id: int, paper_input: PaperCreateInput, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Papers).filter(Papers.id == paper_id)
        result = await session.execute(query)
        paper_update = result.scalar_one_or_none()
        if paper_update:
            paper_update.category = paper_input.category
            paper_update.title = paper_input.title
            paper_update.summary = paper_input.summary
            paper_update.firstParagraph = paper_input.firstParagraph
            paper_update.body = paper_input.body
            paper_update.author_id = paper_input.author_id
            await session.commit()
            return paper_update
        else:
            raise HTTPException(detail='Paper not found', status_code=status.HTTP_404_NOT_FOUND)

@papers_router.get('/{title}', response_model=List[PaperOutput])
async def paper_list(title: str):
    try:
        return await PaperService.search_title(title)
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))



@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(User).filter(User.email == form_data.username)
        result = await session.execute(query)
        user_username = result.scalars().first()

    if user_username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user_username.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    TokenSchema.access_token = create_access_token(user_username.email)
    TokenSchema.refresh_token = create_refresh_token(user_username.email)

    return TokenSchema


