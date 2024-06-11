import os
import base64

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from game import Game

root = os.getenv('ROOT_PATH')

app = FastAPI()
router = APIRouter(prefix=root)

games = {}
class GameRequest(BaseModel):
    board_name: str
    user_name: str

def gen_uid():
    return os.urandom(32).hex()


def gen_bid(board_name):
    return base64.b64encode(board_name.encode()).decode()

@router.get("/create")
async def create(
    game_request: GameRequest
    ):

    bid = gen_bid(game_request.board_name)
    if games.get(bid) == None: 
        game = Game() 
        uid = gen_uid()
        game.uid_link("w", uid, game_request.user_name)
        games[bid] = game
        return JSONResponse(content = {"bid": bid, "uid": uid}, status_code = 200)

    return JSONResponse(content = {"message": "既に存在しています"}, status_code = 404)

@router.get("/join")
async def join():
    pass 


app.include_router(router)