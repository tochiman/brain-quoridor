class UserException(Exception):
    def __str__(self):
        return (
            "白(w)か黒(b)を入力してください。"
        )

class User:
    def __init__(self, color):
        self.wall = 10
        self.color = color
        self.move_list = []

        if self.color == "w":
            self.position = (4, 8)
            self.turn = True
        elif self.color == "b":
            self.position = (4, 0)
            self.turn = False
        else:
            raise UserException

    def reach_goal(self):
        _, y = self.position
        color = self.color
        return self.reach_goal_do(y, color)

    def reach_goal_do(self, y, color):
        if coler == "w":
            if y == 0:
                return True
        else:
            if y == 8:
                return True
        return False 
    
    def check_move(self, x, y): 
        return (x,y) in self.move_list

    def make_move_list(self, board, other_position):
        x, y = self.position
        self.move_list = self.make_move_list_do(x, y, board, other_position)

    def make_move_list_do(self, x, y, board, other_position):
        move_list = []
        if (not [(x-1, y-1), "h"] in board) and (not [(x, y-1), "h"] in board) and (0 <= x <=8 and 0 <= y-1 <= 8): #up　壁がない
            if other_position == (x,y-1): #相手の駒がある
                if (not [(x-1, y-2), "h"] in board) and (not [(x, y-2), "h"] in board) and (0 <= x <=8 and 0 <= y-2 <= 8): #壁がない
                    move_list.append((x,y-2))
                else: #壁がある
                    if (not [(x-1, y-2), "v"] in board) and (not [(x-1, y-1), "v"] in board) and (0 <= x-1 <= 8 and 0 <= y-1 <= 8):
                        move_list.append((x-1, y-1))
                    if (not [(x, y-2), "v"] in board) and (not [(x, y-1), "v"] in board) and (0 <= x+1 <= 8 and 0 <= y-1 <= 8):
                        move_list.append((x+1, y-1))
            else:
                move_list.append((x,y-1))

        if (not [(x-1, y), "h"] in board) and (not [(x, y), "h"] in board) and (0 <= x <=8 and 0 <= y+1 <= 8): #down
            if other_position == (x,y+1):
                if (not [(x-1, y+2), "h"] in board) and (not [(x, y+2), "h"] in board) and (0 <= x <=8 and 0 <= y+2 <= 8): #壁がない
                    move_list.append((x,y+2))
                else: #壁がある
                    if (not [(x-1, y+2), "v"] in board) and (not [(x-1, y+1), "v"] in board) and (0 <= x-1 <= 8 and 0 <= y+1 <= 8):
                        move_list.append((x-1, y+1))
                    if (not [(x, y+2), "v"] in board) and (not [(x, y+1), "v"] in board) and (0 <= x+1 <= 8 and 0 <= y+1 <= 8):
                        move_list.append((x+1, y+1))
            else:
                move_list.append((x,y+1))

        if (not [(x-1, y-1), "v"] in board) and (not [(x-1, y), "v"] in board) and (0 <= x-1 <=8 and 0 <= y <= 8): #left
            if other_position == (x-1,y):
                if (not [(x-2, y-1), "v"] in board) and (not [(x-2, y), "v"] in board) and (0 <= x-2 <=8 and 0 <= y <= 8): #壁がない
                    move_list.append((x-2,y))
                else: #壁がある
                    if (not [(x-2, y-1), "h"] in board) and (not [(x-1, y-1), "h"] in board) and (0 <= x-1 <= 8 and 0 <= y-1 <= 8):
                        move_list.append((x-1, y-1))
                    if (not [(x-2, y), "h"] in board) and (not [(x-1, y), "h"] in board) and (0 <= x-1 <= 8 and 0 <= y+1 <= 8):
                        move_list.append((x-1, y+1))
            else:
                move_list.append((x-1,y))

        if (not [(x, y-1), "v"] in board) and (not [(x, y), "v"] in board) and (0 <= x+1 <=8 and 0 <= y <= 8): #right
            if other_position == (x+1,y):
                if (not [(x+2, y-1), "v"] in board) and (not [(x+2, y), "v"] in board) and (0 <= x+2 <=8 and 0 <= y <= 8): #壁がない
                    move_list.append((x+2,y))
                else: #壁がある
                    if (not [(x+2, y-1), "h"] in board) and (not [(x+1, y-1), "h"] in board) and (0 <= x+1 <= 8 and 0 <= y-1 <= 8):
                        move_list.append((x+1, y-1))
                    if (not [(x+2, y), "h"] in board) and (not [(x+1, y), "h"] in board) and (0 <= x+1 <= 8 and 0 <= y+1 <= 8):
                        move_list.append((x+1, y+1))
            else:
                move_list.append((x+1,y))

        return move_list


    def move(self, x, y):
        self.position = (x, y)

