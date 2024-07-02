from user import User
from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.users = {}
        self.is_start = False

    def uid_link(self, color, uid, user_name):
        self.users[uid] = {"user_name": user_name, "user": User(color), "ws": None}

    def set_ws(self, uid, ws):
        self.users[uid]["ws"] = ws
        count = 0
        for user in users.values():
            if user["ws"] is not None:
                count += 1

        if count == 2:
            return True
        return False
    
    def del_ws(self, uid):
        self.users[uid]["ws"] = None
        count = 0
        for user in users.values():
            if user["ws"] is None:
                count += 1

        if count == 2:
            return True
        return False
