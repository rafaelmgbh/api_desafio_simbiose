from fastapi import APIRouter, HTTPException
from pydantic.class_validators import List

from services import UserService, AuthorService, PaperService
from schemas import UserCreateInput, StandardOutput, UserListOutput, AuthorCreateInput, AuthorlistOutput, \
    PaperCreateInput, AuthorUpdateInput, PaperOutput
import logging

user_router = APIRouter(prefix='/user')
author_router = APIRouter(prefix='/authors')
papers_router = APIRouter(prefix='/papers')


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


@user_router.get('/list/', response_model=List[UserListOutput])
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
async def up_author(author_id: int, author_input: AuthorUpdateInput):
    try:
        return AuthorService.update_author(author_id, author_input)
    except Exception as erro:
        raise HTTPException(400, detail=str(erro))


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
