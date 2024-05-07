from fastapi import FastAPI
import os

app = FastAPI()

root = os.getenv('ROOT_PATH')

@app.get("%s" % root)
async def root():
    return {"message": "Hello World"}
