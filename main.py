from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()


# uvicorn main:app --port 8080 --reload
@router.get('/')
def first():
    return 'Hello world!'

app.include_router(prefix='/first', router=router)