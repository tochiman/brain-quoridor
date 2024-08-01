from user import User
from copy import deepcopy

class Game:
    def __init__(self):
        self.board = []
        self.users = {}
        self.is_start = False

    def put_wall(self, x, y, wall_type, uid):
        self.board.append([(x,y), wall_type])
        self.users[uid]["user"].wall -= 1


    def check_wall(self, x, y, wall_type, uid):
        if self.users[uid]["user"].wall == 0:
            return False
        if not (0 <= x <= 8 and 0 <= y <= 8):
            return False
        for board in self.board:
            if board[0] == (x,y):
                return False
            if board[1] == wall_type:
                if wall_type == "h"
                    if board[0] == (x+1,y) or board[0] == (x-1, y):
                        return False
                elif wall_type == "v"
                    if board[0] == (x,y+1) or board[0] == (x,y-1):
                        return False

        return bfs(x, y, wall_type):

    def bfs(self, x, y, wall_type):
        b = deepcopy(self.board)
        b.append([(x, y), wall_type])
        result = [False, False]
        for index, _user in enumerate(self.users.values()):
            user = _user["user"]
            color = user.color
            l = deepcopy(user.move_list)
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

    def uid_link(self, color, uid, user_name):
        self.users[uid] = {"user_name": user_name, "user": User(color), "ws": None}
        
    def notify_ws(self, uid = None):
        users = []
        for user in self.users.values():
            users.append(user)
        for index, _user in enumerate(users):
            ws = _user["ws"]
            user = _user["user"]
            if uid is not None :
                if users[uid] != user:
                    continue
            other = users[(index+1) % 2]["user"]
            if user.trun == True:
                ws.send_json({
                    "trun": user.trun, 
                    "position": user.position, 
                    "other_position": other.position, 
                    "wall": user.wall,
                    "other_wall": other.wall,
                    "color": user.color,
                    "move_list": user.move_list,
                    "board": self.board
                    })
            else:
                ws.send_json({
                    "trun": user.trun, 
                    "position": user.position, 
                    "other_position": other.position, 
                    "wall": user.wall,
                    "other_wall": other.wall,
                    "color": user.color,
                    "board": self.board
                    })


    def set_ws(self, uid, ws):
        self.users[uid]["ws"] = ws
        count = 0
        for user in self.users.values():
            if user["ws"] is not None:
                count += 1

        if count == 2:
            return True
        return False
    
    def del_ws(self, uid):
        self.users[uid]["ws"] = None
        count = 0
        for user in self.users.values():
            if user["ws"] is None:
                count += 1

        if count == 2:
            return True
        return False

