import os
import base64
import asyncio
import datetime

from fastapi import FastAPI, APIRouter, Cookie, WebSocket, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from game import Game
            
from logging import getLogger, StreamHandler
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

root = os.getenv('ROOT_PATH')

app = FastAPI()
router = APIRouter(prefix=root)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


games = {}
class GameRequest(BaseModel):
    board_name: str
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


def gen_uid():
    return os.urandom(32).hex()


def gen_bid(board_name):
    return base64.b64encode(board_name.encode()).decode()


@router.post("/create")
async def create(
    game_request: GameRequest
    ):

    bid = gen_bid(game_request.board_name)
    new_game = False
    game = games.get(bid)
    if game == None:
        new_game = True
    else:
        is_del = game.is_del()
        if is_del:
            del games[bid]
            new_game = True
    if new_game:
        game = Game()
        game.set_item()
        uid = gen_uid()
        game.link_uid("w", uid, game_request.user_name)
        games[bid] = game
        response = JSONResponse(content = {"message": "作成しました"}, status_code = 200)
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        response.set_cookie(key="bid", value=bid, secure=True, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        response.set_cookie(key="uid", value=uid, secure=True, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
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
    bid = gen_bid(game_request.board_name)
    game = games.get(bid)
    if game is not None:
        if not game.is_start:
            uid = gen_uid()
            game.link_uid("b", uid, game_request.user_name)
            game.set_is_start()
            await game.notify_ws()

            response = JSONResponse(content = {"message": "参加しました"}, status_code = 200)
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            response.set_cookie(key="bid", value=bid, secure=True, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            response.set_cookie(key="uid", value=uid, secure=True, httponly=True, samesite='strict', expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            return response
        else:
            if bid == cbid and cuid in game.users.keys():
                return JSONResponse(content = {"message": "参加しました"}, status_code = 200)

    return JSONResponse(content = {"message": "ゲームに参加できません"}, status_code = 400)


@router.post("/move")
async def move(
    move_request: MoveRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]
    x = move_request.x
    y = move_request.y
    if (user.turn and not game.turn_guard) or game.move_everyone:
        game.set_turn_guard()
        check_move = user.check_move(x,y)
        if check_move:
            user.move(x,y)
            if game.check_item_position(x, y):
                game.link_item(x, y, uid)

            if user.reach_goal():
                await game.win(uid)
                del games[bid]
                return JSONResponse(content = {"message": "ゲームが終了しました"}, status_code = 200)
            
            other = game.get_other(uid)["user"]
            user.make_move_list(game.board, other.position)
            other.make_move_list(game.board, user.position)

            if game.move_everyone:
                game.unset_move_everyone()
            elif game.twice:
                game.unset_twice()
                game.unset_turn_guard()
            else: 
                game.unset_move_everyone_guard()
                game.unset_twice_guard()
                game.count_turn()
                game.unset_turn_guard()
            await game.notify_ws()
            return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "その場所に動くことはできません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/wall")
async def wall(
    wall_request: WallRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]
    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_wall = game.check_wall(x, y, wall_type, uid)
        if check_wall:
            game.put_wall(x, y, wall_type, uid)
    
            other = game.get_other(uid)["user"]
            user.make_move_list(game.board, other.position)
            other.make_move_list(game.board, user.position)
            
            if game.twice:
                game.unset_twice()
            else: 
                game.unset_twice_guard()
                game.count_turn()

            game.unset_turn_guard()
            await game.notify_ws()
            return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "その場所に壁を置けません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/get_wall")
async def get_wall(
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)

    if game.twice_guard:
        return JSONResponse(content = {"message": "このアイテム使用中はアイテムの使用ができません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_item = user.check_item("get_wall")
        if check_item:
            user.add_wall()
            user.remove_item("get_wall")
            game.count_turn()
            
            await game.notify_ws()
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "このアイテムは使えません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/break_wall")
async def break_wall(
    wall_request: WallRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]

    x = wall_request.x
    y = wall_request.y
    wall_type = wall_request.wall_type

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)

    if game.twice_guard:
        return JSONResponse(content = {"message": "このアイテム使用中はアイテムの使用ができません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_item = user.check_item("break_wall")
        if check_item:
            if game.is_wall(x, y, wall_type):
                game.delete_wall(x, y, wall_type)
                user.remove_item("break_wall")

                other = game.get_other(uid)["user"]
                user.make_move_list(game.board, other.position)
                other.make_move_list(game.board, user.position)

                game.count_turn()
            
                await game.notify_ws()
                game.unset_turn_guard()
                return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
            else:
                game.unset_turn_guard()
                return JSONResponse(content = {"message": "壁は存在しません"}, status_code = 400)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "このアイテムは使えません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/replace_wall")
async def replace_wall(
    item_wall_request: ItemWallRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]

    #移動前
    x1 = item_wall_request.x1
    y1 = item_wall_request.y1
    wall_type1 = item_wall_request.wall_type1
    #移動後
    x2 = item_wall_request.x2
    y2 = item_wall_request.y2
    wall_type2 = item_wall_request.wall_type2

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)
    
    if game.twice_guard:
        return JSONResponse(content = {"message": "このアイテム使用中はアイテムの使用ができません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_item = user.check_item("replace_wall")
        if check_item:
            if game.is_wall(x1, y1, wall_type1):
                game.delete_wall(x1, y1, wall_type1)
                check_wall = game.check_wall(x2, y2, wall_type2)
                if check_wall:
                    game.put_wall(x2, y2, wall_type2)
                    user.remove_item("replace_wall")
            
                    other = game.get_other(uid)["user"]
                    user.make_move_list(game.board, other.position)
                    other.make_move_list(game.board, user.position)

                    game.count_turn()

                    await game.notify_ws()
                    game.unset_turn_guard()
                    return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
                else:
                    game.put_wall(x1, y1, wall_type1)
                    game.unset_turn_guard()
                    return JSONResponse(content = {"message": "その場所に壁は置けません"}, status_code = 400)
            else:
                game.unset_turn_guard()
                return JSONResponse(content = {"message": "壁が存在しません"}, status_code = 400)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "このアイテムは使えません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/twice")
async def twice(
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)
    
    if game.twice_guard:
        return JSONResponse(content = {"message": "このアイテム使用中はアイテムの使用ができません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_item = user.check_item("twice")
        if check_item:
            game.set_twice()
            user.remove_item("twice")
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "このアイテムは使えません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.post("/move_everyone")
async def move_everyone(
    move_request: MoveRequest,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    game = games.get(bid)
    if game is None:
        return JSONResponse(content = {"message":"ゲームが存在しません"}, status_code=400)
    user = game.get_user(uid)["user"]

    if game.move_everyone_guard:
        return JSONResponse(content = {"message": "このアイテム使用中は駒を動かすことしかできません"}, status_code = 400)
    
    if game.twice_guard:
        return JSONResponse(content = {"message": "このアイテム使用中はアイテムの使用ができません"}, status_code = 400)

    if user.turn and not game.turn_guard:
        game.set_turn_guard()
        check_item = user.check_item("move_everyone")
        if check_item:
            other_uid = game.get_other_uid(uid)
            game.set_move_everyone()
            await move(move_request, bid, other_uid)
            user.remove_item("move_everyone")
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "正常に処理しました"}, status_code=200)
        else:
            game.unset_turn_guard()
            return JSONResponse(content = {"message": "このアイテムは使えません"}, status_code = 400)
    return JSONResponse(content = {"message": "あなたのターンではありません"}, status_code = 400)


@router.websocket("/ws")
async def websocket(
    ws: WebSocket,
    bid: str | None = Cookie(default = None),
    uid: str | None = Cookie(default = None)
    ):
    await ws.accept()
    game = games.get(bid)
    if game is not None:
        if uid in game.users.keys():
            game.set_ws(uid, ws)
            if game.is_start:
                await game.notify_ws(uid)
            while True:
                await asyncio.sleep(10)
                try:
                    await ws.send_json({"message": "ping"})
                except:
                    _ws = game.get_user(uid)["ws"]
                    if _ws == ws:
                        game.del_ws(uid)
                        is_del = game.is_del()
                        if is_del:
                            del games[bid]


app.include_router(router)
