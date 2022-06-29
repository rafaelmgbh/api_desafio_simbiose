from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.class_validators import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from core.deps import get_session, get_hashed_password
from core.security import get_hash_pwd
from database.models import Author, User

from database.connection import Session
from services import UserService, AuthorService, PaperService
from schemas import UserCreateInput, StandardOutput, UserListOutput, AuthorCreateInput, AuthorlistOutput, \
    PaperCreateInput, AuthorUpdateInput, PaperOutput, UserOut, UserCreate
import logging

user_router = APIRouter(prefix='/user')
author_router = APIRouter(prefix='/authors')
papers_router = APIRouter(prefix='/papers')
auth_router = APIRouter(prefix='/auth')


@user_router.post('/create', description="Create user end point", summary="Create User", response_model=StandardOutput)
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@user_router.delete('/delete/{user_id}', response_model=StandardOutput)
async def user_create(user_id: int):
    try:
        await UserService.delete_user(user_id)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@user_router.get('/list/', response_model=List[UserOut])
async def user_list():
    try:
        return await UserService.list_user()
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@author_router.post('/create', response_model=StandardOutput)
async def author_create(author_input: AuthorCreateInput):
    try:
        await AuthorService.create_author(author_input)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@author_router.get('/list/', response_model=List[AuthorlistOutput])
async def author_list():
    try:
        return await AuthorService.list_author()
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@author_router.put('/ATUALIZACAO/{author_id}')
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


@author_router.get('/{name}', response_model=List[AuthorlistOutput])
async def author_list(name):
    try:
        return await AuthorService.search_author(name)
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@papers_router.get('/{title}', response_model=List[PaperOutput])
async def paper_list(title: str):
    try:
        return await PaperService.search_title(title)
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


@papers_router.post('/create', response_model=StandardOutput)
async def create_paper(paper_input: PaperCreateInput):
    try:
        await PaperService.create_paper(paper_input)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


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
