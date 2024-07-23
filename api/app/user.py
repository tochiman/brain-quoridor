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
            self.turn = True
        elif self.color == "b":
            self.position = (4, 0)
            self.turn = False
        else:
            raise UserException

    def reach_goal(self):
        _,y = self.position
        if self.coler == "w":
            if y == 0:
                return True
        else:
            if y == 8:
                return True
        return False 
    
    def check_move(self, x, y, board, other_position): #次ここから　動けるかどうかを判定
        x,y = self.position
        if 
        move_list = []


    def move(self, x, y):
        self.position = (x, y)

    
