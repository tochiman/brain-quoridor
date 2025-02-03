import os
import asyncio
import hashlib
import json
import datetime

from fastapi import FastAPI, APIRouter, Cookie, WebSocket, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from game import Mode
            
from logging import getLogger, StreamHandler
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

root = os.getenv('ROOT_PATH')

app = FastAPI()
router = APIRouter(prefix=root)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quoridor.k175.net", "http://192.168.100.170"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


games = {}

class GameRequest(BaseModel):
    room_name: str
    user_name: str


class MoveRequest(BaseModel):
    x: int
    y: int


class WallRequest(BaseModel):
    x: int
    y: int
    wall_type: str


class ItemWallRequest(BaseModel):
    x1: int
    y1: int
    wall_type1: str
    x2: int
    y2: int
    wall_type2: str


def gen_bid(room_name):
    return hashlib.sha512(room_name.encode("utf-8")).hexdigest()


def gen_id():
    return os.urandom(32).hex()


@router.post("/ai")
async def ai():
    bid = gen_id()
    game = games.get(bid)
    if game is None:
        game = Mode()
        uid = gen_id()
        game.set_is_start()
        game.set_player(2, uid) 
        game.set_item_position()
        games[bid] = game

        response = JSONResponse(content = {"message": "作成しました"}, status_code = 200)
        response.set_cookie(key="bid", value=bid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        response.set_cookie(key="uid", value=uid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        return response

    return JSONResponse(content = {"message": "既に存在しています"}, status_code = 400)

@router.post("/create")
async def create(
    game_request: GameRequest
    ):

    bid = gen_bid(game_request.room_name)
    game = games.get(bid)

    if game:
        if game.is_del():
            del games[bid]
            game = None

    if game is None:
        game = Mode(game_request.room_name)
        uid = gen_id()
        game.set_player(0, uid, game_request.user_name) 
        game.set_item_position()
        games[bid] = game
        response = JSONResponse(content = {"message": "作成しました"}, status_code = 200)
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        response.set_cookie(key="bid", value=bid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        response.set_cookie(key="uid", value=uid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        return response

    return JSONResponse(content = {"message": "既に存在しています"}, status_code = 400)


@router.post("/join")
async def join(
    game_request: GameRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    cbid = bid
    cuid = uid
    bid = gen_bid(game_request.room_name)
    game = games.get(bid)
    if game is not None:
        if not game.is_start:
            uid = gen_id()
            game.set_player(1, uid, game_request.user_name)
            game.set_is_start()
            await game.notify_ws()

            response = JSONResponse(content = {"message": "参加しました"}, status_code = 200)
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            response.set_cookie(key="bid", value=bid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            response.set_cookie(key="uid", value=uid, secure=False, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            return response
        else:
            if bid == cbid and cuid in game.uids:
                return JSONResponse(content = {"message": "参加しました"}, status_code = 200)

    return JSONResponse(content = {"message": "ゲームに参加できません"}, status_code = 400)


@router.post("/move")
async def move(
    move_request: MoveRequest,
    background_tasks: BackgroundTasks,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    x = move_request.x
    y = move_request.y

    status = await game.run(uid, "move", x, y)
    background_tasks.add_task(game.run_ai)

    if status == 0:
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
    elif status == 1:
        return JSONResponse(content = {"message": "その場所に動くことはできません"}, status_code = 400)
    elif status == 2:
        return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)
    elif status == 3:
        return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)

@router.post("/wall")
async def wall(
    wall_request: WallRequest,
    background_tasks: BackgroundTasks,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    status = await game.run(uid, "wall", x, y, wall_type)
    background_tasks.add_task(game.run_ai)

    if status == 0:
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
    elif status == 1:
        return JSONResponse(content = {"message": "その場所に壁を置けません"}, status_code = 400)
    elif status == 2:
        return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)
    elif status == 3:
        return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)

@router.post("/free_wall")
async def free_wall(
    wall_request: WallRequest,
    background_tasks: BackgroundTasks,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    status = await game.run(uid, "free_wall", x, y, wall_type)
    background_tasks.add_task(game.run_ai)

    if status == 0:
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
    elif status == 1:
        return JSONResponse(content = {"message": "その場所に壁を置けません"}, status_code = 400)
    elif status == 2:
        return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)
    elif status == 3:
        return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)


@router.post("/break_wall")
async def free_wall(
    wall_request: WallRequest,
    background_tasks: BackgroundTasks,

    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)

    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    status = await game.run(uid, "break_wall", x, y, wall_type)
    background_tasks.add_task(game.run_ai)

    if status == 0:
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
    elif status == 1:
        return JSONResponse(content = {"message": "その壁は壊せません"}, status_code = 400)
    elif status == 2:
        return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)
    elif status == 3:
        return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)


@router.post("/twice")
async def move(
    move_request: MoveRequest,
    background_tasks: BackgroundTasks,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)

    x = move_request.x
    y = move_request.y

    status = await game.run(uid, "twice", x, y)
    background_tasks.add_task(game.run_ai)

    if status == 0:
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
    elif status == 1:
        return JSONResponse(content = {"message": "その場所に動くことはできません"}, status_code = 400)
    elif status == 2:
        return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)
    elif status == 3:
        return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)


@router.post("/surrender")
async def surrender(
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)

    if game.get_user(uid):
        await game.lose(uid)
        return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)

    return JSONResponse(content = {"message":"ユーザが存在しません"}, status_code=400)
    
@router.get("/info")
async def get_info(
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)    
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)

    if game.get_user(uid):
        info = game.get_info(uid)
        return JSONResponse(content = info, status_code=200)

    return JSONResponse(content = {"message":"ユーザが存在しません"}, status_code=400)

@router.websocket("/ws")
async def websocket(
    ws: WebSocket,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    await ws.accept()
    game = games.get(bid)

    if game is None:
        return
    if uid not in game.uids:
        return 

    game.set_ws(uid, ws)
    if game.is_start:
        await game.notify_ws(uid)
    while True:
        try:
            data = await ws.receive_text()
            await ws.send_json({"message":"pong"})
        except:
            _ws = game.get_ws(uid)
            if _ws == ws:
                game.del_ws(uid)
                is_del = game.is_del()
                if is_del:
                    del games[bid]
                await ws.close()


app.include_router(router)
