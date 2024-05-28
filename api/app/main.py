from fastapi import FastAPI, APIRouter
import os

root = os.getenv('ROOT_PATH')

app = FastAPI()
router = APIRouter(prefix=root)

@router.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router)