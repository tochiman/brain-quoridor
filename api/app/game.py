from copy import deepcopy
import random

from user import User

class Game:
    def __init__(self):
        self.board = []
        self.users = {}
        self.is_start = False
        self.items = {}
        self.item_list = ["get_wall", "break_wall", "replace_wall", "twice", "move_everyone"]
        self.twice = False
        self.twice_guard = False
        self.move_everyone = False
        self.move_everyone_guard = False
        self.turn_guard = False


    def put_wall(self, x, y, wall_type, uid = None):
        self.board.append([(x, y), wall_type])
        if uid is not None:
            self.users[uid]["user"].wall -= 1


    def check_wall(self, x, y, wall_type, uid = None):
        if uid is not None:
            if self.users[uid]["user"].wall == 0:
                return False
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False
        if wall_type not in ["v", "h"]:
            return False
        for board in self.board:
            if board[0] == (x, y):
                return False
            if board[1] == wall_type:
                if wall_type == "h":
                    if board[0] == (x+1, y) or board[0] == (x-1, y):
                        return False
                elif wall_type == "v":
                    if board[0] == (x, y+1) or board[0] == (x, y-1):
                        return False

        return self.bfs(x, y, wall_type)


    def bfs(self, x, y, wall_type):
        b = deepcopy(self.board)
        b.append([(x, y), wall_type])
        result = [False, False]
        for index, _user in enumerate(self.users.values()):
            user = _user["user"]
            color = user.color
            l = user.make_move_list_do(user.position[0], user.position[1], b, ())

            for i in l:
                x, y = i
                if user.reach_goal_do(y, color):
                   result[index] = True
                   break
                tmp = user.make_move_list_do(x, y, b, ())
                for t in tmp:
                    if not t in l:
                        l.append(t)
        return (result[0] and result[1])


    def get_user(self, uid):
        return self.users[uid]


    def get_other(self, uid):
        uid = self.get_other_uid(uid)
        return self.users[uid]


    def get_other_uid(self, uid):
        other_uid = ""
        for _uid in self.users.keys():
            if _uid == uid:
                continue
            other_uid = _uid
        return other_uid


    def count_turn(self):
        for _user in self.users.values():
            user = _user["user"]
            user.count_turn()


    async def win(self, uid):
        user = self.get_user(uid)["ws"]
        other = self.get_other(uid)["ws"]

        await user.send_json({"message":"勝利！"})
        await other.send_json({"message":"敗北..."})


    def link_uid(self, color, uid, user_name):
        self.users[uid] = {"user_name": user_name, "user": User(color), "ws": None}


    def set_is_start(self):
        self.is_start = True


    async def notify_ws(self, uid = None):
        for _uid, _user in self.users.items():
            ws = _user["ws"]
            if ws is not None:
                if uid is not None :
                    if uid != _uid:
                        continue
                user = _user["user"]
                _other = self.get_other(_uid)
                other = _other["user"]
                if user.turn:
                    await ws.send_json({
                        "name": _user["user_name"],
                        "other_name": _other["user_name"],
                        "turn": user.turn, 
                        "position": user.position, 
                        "other_position": other.position, 
                        "wall": user.wall,
                        "other_wall": other.wall,
                        "color": user.color,
                        "move_list": user.move_list,
                        "other_move_list": other.move_list,
                        "board": self.board,
                        "item_position": [item for item in self.items.keys()],
                        "item": user.items,
                        "other_item": other.items
                        })
                else:
                    await ws.send_json({
                        "name": _user["user_name"],
                        "other_name": _other["user_name"],
                        "turn": user.turn, 
                        "position": user.position, 
                        "other_position": other.position, 
                        "wall": user.wall,
                        "other_wall": other.wall,
                        "color": user.color,
                        "board": self.board,
                        "item_position": [item for item in self.items.keys()],
                        "item": user.items,
                        "other_item": other.items
                        })


    def set_ws(self, uid, ws):
        self.users[uid]["ws"] = ws


    def del_ws(self, uid):
        self.users[uid]["ws"] = None


    def is_del(self):
        count = 0
        for user in self.users.values():
            if user["ws"] is None:
                count += 1

        if count == len(self.users):
            return True
        return False


    def set_item(self):
        item = random.sample(self.item_list, 2)
        self.items[(2, 2)] = item[0]
        self.items[(6, 6)] = item[0]
        self.items[(4, 4)] = item[1]

    
    def check_item_position(self, x, y):
        return (x, y) in self.items.keys()

    
    def link_item(self, x, y, uid):
        user = self.get_user(uid)["user"]
        item = self.items[(x, y)]
        user.set_item(item)
        del self.items[(x, y)]


    def is_wall(self, x, y, wall_type):
        return [(x, y), wall_type] in self.board


    def delete_wall(self, x, y, wall_type):
        self.board.remove([(x, y), wall_type])


    def set_twice(self):
        self.twice = True
        self.twice_guard = True


    def unset_twice(self):
        self.twice = False


    def unset_twice_guard(self):
        self.twice_guard = False

    
    def set_move_everyone(self):
        self.move_everyone = True
        self.move_everyone_guard = True


    def unset_move_everyone(self):
        self.move_everyone = False


    def unset_move_everyone_guard(self):
        self.move_everyone_guard = False


    def set_turn_guard(self):
        self.move_everyone_guard = True


    def unset_turn_guard(self):
        self.move_everyone_guard = False
