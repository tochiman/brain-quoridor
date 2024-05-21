class UserException(Exception):
    def __str__(self):
        return (
            "白(w)か黒(b)を入力してください。"
        )

class User:
    def __init__(self, color):
        self.wall = 10
        self.color = color
        self.movable = []
        self.can_put_wall = []

        if self.color == "w":
            self.position = (4, 8)
            self.turn = 1
        elif self.color == "b":
            self.position = (4, 0)
            self.turn = 0
        else:
            raise UserException

