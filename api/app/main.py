import os
import base64
import asyncio

from fastapi import FastAPI, APIRouter, Cookie, WebSocket
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
async def join(
    game_request: GameRequest,
    cbid: str | None = Cookie(default = None),
    cuid: str | None = Cookie(default = None)
    ):
    bid = gen_bid(game_request.board_name)
    game = games.get(bid)
    if game is not None:
        if game.is_start == False:
            uid = gen_bid()
            game.uid_link("b", uid, game_request.user_name)
            return JSONResponse(content = {"bid": bid, "uid": uid}, status_code = 200)
        else:
            if bid == cbid:
                return JSONResponse(content = {"bid": cbid, "uid": cuid}, status_code = 200)

    return JSONResponse(content = {"message": "ゲームに参加できません"}, status_code = 404)

@router.websocket("/ws")
async def websocket(
    ws: WebSocket,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    await ws.accept()
    game = games.get(bid)
    is_start = game.set_ws(uid, ws)
    if game.is_start == False and is_start == True: #接続
        game.is_strat = is_start
        game.notify_ws()
    elif game.is_start == True and is_start == True: #再接続
        game.notify_ws(uid)
    while True:
        await asyncio.sleep(10)
        try:
            await asyncio.wait_for(ws.receive_text(), timeout = 5)
        except:
            await ws.close()
            is_del = del_ws(uid)
            if is_del == True:
                del games[bid]


app.include_router(router)