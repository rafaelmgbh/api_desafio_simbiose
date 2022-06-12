from fastapi import FastAPI, APIRouter
from views import user_router

app = FastAPI()
router = APIRouter()


# source venv/bin/activate && set -a; source .env; set +a
# uvicorn main:app --port 8080 --reload
@router.get('/')
def first():
    return 'Hello world!'


app.include_router(prefix='/first', router=router)
app.include_router(user_router)
