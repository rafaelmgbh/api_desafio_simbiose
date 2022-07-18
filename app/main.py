import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.responses import RedirectResponse

from views import user_router,author_router, papers_router

# to get a string like this run:
# openssl rand -hex 32

app = FastAPI()
app.title = "The Libray API"
router = APIRouter()

# docker compose up-
# source venv/bin/activate && set -a; source .env; set +a


app.include_router(user_router)
app.include_router(author_router)
app.include_router(papers_router)

api_get = APIRouter()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs/')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, debug=True, reload=True)
