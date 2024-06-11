from user import User
from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.users = {}
        self.is_start = False

    def uid_link(self, color, uid, user_name):
        self.users[uid] = {"user_name": user_name, "user": User(color)}
