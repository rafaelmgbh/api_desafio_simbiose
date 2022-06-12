from fastapi import APIRouter , HTTPException
from services import UserService
from schemas import UserCreateInput, StandardOutput, ErrorOutput
import logging

user_router = APIRouter(prefix='/user')


@user_router.post('/create', response_model=StandardOutput)
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
        logging.info('Sucess !')
        return StandardOutput(message='Ok')
    except Exception as erro :
        raise HTTPException(400, detail=str(erro))
