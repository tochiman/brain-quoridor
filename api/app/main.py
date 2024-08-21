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

class MoveRequest(BaseModel):
    x: int
    y: int

class WallRequest(BaseModel):
    x: int
    y: int
    wall_type: str



@router.post("/create")
async def create(
    game_request: GameRequest
    ):

    bid = gen_bid(game_request.board_name)
    new_game = False
    if games.get(bid) == None: 
        new_game = True
    else:
        count = 0
        users = games.get(bid).users
        for user in users.values():
            if user["ws"] == None:
                cout += 1
        if count == len(users):
            del games[bid]
            new_game = True
    if new_game:
        game = Game() 
        uid = gen_uid()
        game.uid_link("w", uid, game_request.user_name)
        games[bid] = game
        return JSONResponse(content = {"bid": bid, "uid": uid}, status_code = 200)

    return JSONResponse(content = {"message": "既に存在しています"}, status_code = 404)

@router.post("/join")
async def join(
    game_request: GameRequest,
    cbid: str | None = Cookie(default = None),
    cuid: str | None = Cookie(default = None)
    ):
    bid = gen_bid(game_request.board_name)
    game = games.get(bid)
    if game is not None:
        if game.is_start == False:
            uid = gen_uid()
            game.uid_link("b", uid, game_request.user_name)
            return JSONResponse(content = {"bid": bid, "uid": uid}, status_code = 200)
        else:
            if bid == cbid:
                return JSONResponse(content = {"bid": cbid, "uid": cuid}, status_code = 200)

    return JSONResponse(content = {"message": "ゲームに参加できません"}, status_code = 404)




@router.post("/move")
async def move(
    move_request: MoveRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    user = game.get_user(uid)["user"]
    x = move_request.x
    y = move_request.y
    if user.turn == True:

        check_move = user.check_move(x,y)
        if check_move == True:
            user.move(x,y)
            if user.reach_goal() == True:
                pass #ゴール時の処理
            game.count_turn(uid)
        
            other = game.get_other(uid)["user"]
            other.make_move_list(game.board, user.position)

            await game.notify_ws()




@router.post("/wall")
async def wall(
    wall_request: WallRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    user = game.get_user(uid)["user"]
    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    if user.turn == True:
        check_wall = game.check_wall(x, y, wall_type, uid)
        if check_wall == True:
            game.put_wall(x, y, wall_type, uid)
            game.count_turn(uid)

            other = game.get_other(uid)["user"]
            other.make_move_list(game.board, user.position)
            await game.notify_ws()





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
        game.set_is_start()
        await game.notify_ws()
    elif game.is_start == True and is_start == True: #再接続
        await game.notify_ws(uid)
    while True:
        await asyncio.sleep(10)
        try:
            await asyncio.wait_for(ws.receive_text(), timeout = 10)
        except:
            await ws.close()
            is_del = game.del_ws(uid)
            if is_del == True:
                del games[bid]


app.include_router(router)
