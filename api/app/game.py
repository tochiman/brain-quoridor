import math
import random
from copy import deepcopy
import asyncio

from logging import getLogger, StreamHandler
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
class QuoridorState:
    def __init__(self):
        self.board = []
        self.player_positions =[(4,0), (4,8)]
        self.walls =[10, 10]
        self.current_player = 0
        self.move_count = 0


    def copy(self):
        new_state = QuoridorState()
        new_state.board = self.board[:]
        new_state.player_positions = self.player_positions[:]
        new_state.walls = self.walls[:]
        new_state.current_player = self.current_player
        new_state.move_count = self.move_count
        return new_state

    def make_move_list(self, x, y, other_position):
        return self.make_move_list_do(x, y, self.board, other_position)
    
    def make_move_list_do(self, x, y, board, other_position):
        moves = []
        if (not (x-1, y-1, "h") in board) and (not (x, y-1, "h") in board) and (0 <= x <= 8 and 0 <= y-1 <= 8): #up　壁がない
            if other_position == (x, y-1): #相手の駒がある
                if (not (x-1, y-2, "h") in board) and (not (x, y-2, "h") in board) and (0 <= x <= 8 and 0 <= y-2 <= 8): #壁がない
                    moves.append(("move", x, y-2))
                else: #壁がある
                    if (not (x-1, y-2, "v") in board) and (not (x-1, y-1, "v") in board) and (0 <= x-1 <= 8 and 0 <= y-1 <= 8):
                        moves.append(("move", x-1, y-1))
                    if (not (x, y-2, "v") in board) and (not (x, y-1, "v") in board) and (0 <= x+1 <= 8 and 0 <= y-1 <= 8):
                        moves.append(("move", x+1, y-1))
            else:
                moves.append(("move", x, y-1))

        if (not (x-1, y, "h") in board) and (not (x, y, "h") in board) and (0 <= x <= 8 and 0 <= y+1 <= 8): #down
            if other_position == (x, y+1):
                if (not (x-1, y+1, "h") in board) and (not (x, y+1, "h") in board) and (0 <= x <= 8 and 0 <= y+2 <= 8): #壁がない
                    moves.append(("move", x, y+2))
                else: #壁がある
                    if (not (x-1, y+1, "v") in board) and (not (x-1, y, "v") in board) and (0 <= x-1 <= 8 and 0 <= y+1 <= 8):
                        moves.append(("move", x-1, y+1))
                    if (not (x, y+1, "v") in board) and (not (x, y, "v") in board) and (0 <= x+1 <= 8 and 0 <= y+1 <= 8):
                        moves.append(("move", x+1, y+1))
            else:
                moves.append(("move", x, y+1))

        if (not (x-1, y-1, "v") in board) and (not (x-1, y, "v") in board) and (0 <= x-1 <= 8 and 0 <= y <= 8): #left
            if other_position == (x-1, y):
                if (not (x-2, y-1, "v") in board) and (not (x-2, y, "v") in board) and (0 <= x-2 <= 8 and 0 <= y <= 8): #壁がない
                    moves.append(("move", x-2, y))
                else: #壁がある
                    if (not (x-2, y-1, "h") in board) and (not (x-1, y-1, "h") in board) and (0 <= x-1 <= 8 and 0 <= y-1 <= 8):
                        moves.append(("move", x-1, y-1))
                    if (not (x-2, y, "h") in board) and (not (x-1, y, "h") in board) and (0 <= x-1 <= 8 and 0 <= y+1 <= 8):
                        moves.append(("move", x-1, y+1))
            else:
                moves.append(("move", x-1, y))

        if (not (x, y-1, "v") in board) and (not (x, y, "v") in board) and (0 <= x+1 <= 8 and 0 <= y <= 8): #right
            if other_position == (x+1, y):
                if (not (x+1, y-1, "v") in board) and (not (x+1, y, "v") in board) and (0 <= x+2 <= 8 and 0 <= y <= 8): #壁がない
                    moves.append(("move", x+2, y))
                else: #壁がある
                    if (not (x+1, y-1, "h") in board) and (not (x, y-1, "h") in board) and (0 <= x+1 <= 8 and 0 <= y-1 <= 8):
                        moves.append(("move", x+1, y-1))
                    if (not (x+1, y, "h") in board) and (not (x, y, "h") in board) and (0 <= x+1 <= 8 and 0 <= y+1 <= 8):
                        moves.append(("move", x+1, y+1))
            else:
                moves.append(("move", x+1, y))
        return moves

    def check_wall(self, x, y, wall_type):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False
        if wall_type not in ["v", "h"]:
            return False
        for board in self.board:
            if board[0:2] == (x, y):
                return False
            if board[2] == wall_type:
                if wall_type == "h":
                    if board[0:2] == (x+1, y) or board[0:2] == (x-1, y):
                        return False
                elif wall_type == "v":
                    if board[0:2] == (x, y+1) or board[0:2] == (x, y-1):
                        return False

        return self.bfs(x, y, wall_type)
    
    def bfs(self, x, y, wall_type):
        b = deepcopy(self.board)
        b.append((x, y, wall_type))
        result = [False, False]
        for index in range(2):
            x, y = self.player_positions[index]
            l = self.make_move_list_do(x, y, b, ())
            for i in l:
                _, x, y = i
                if y == (1-index) * 8:
                    result[index] = True
                    break
                tmp = self.make_move_list_do(x, y, b, ())
                for t in tmp:
                    if not t in l:
                        l.append(t)
        return (result[0] and result[1])

    def get_legal_moves(self, flag=True):
        return self.get_legal_moves_do(self.current_player, flag)
    
    def get_legal_moves_do(self, player, flag=True):
        moves = []
        # 駒の移動
        x, y = self.player_positions[player]
        other_position = self.player_positions[1 - player]
        moves = self.make_move_list(x, y, other_position)

        # 壁の設置
        if self.move_count // 2 > 2 or flag:
            if self.walls[player] > 0:
                for i in range(8):
                    for j in range(8):
                        for k in ["v", "h"]:
                            if self.check_wall(i, j, k):
                                moves.append(('wall', i, j, k))
            
        return moves


    def make_move(self, move):
        if move[0] == 'move':
            self.player_positions[self.current_player] = (move[1], move[2])
        elif move[0] == 'wall':
            self.walls[self.current_player] -= 1
            self.board.append((move[1], move[2], move[3]))
        self.current_player = 1 - self.current_player
        self.move_count += 1

    def is_terminal(self):
        return self.player_positions[0][1] == 8 or self.player_positions[1][1] == 0

    def get_result(self):
        if self.player_positions[0][1] == 8:
            return -1
        elif self.player_positions[1][1] == 0:
            return 1
        return 0


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children= []
        self.visits = 0
        self.value = 0

    def evaluate_early_moves(self):
        # 序盤2手以内の前進を評価
        if self.state.move_count // 2 <= 2:
            current_y = self.state.player_positions[1 - self.state.current_player][1]
            if self.parent:
                previous_y = self.parent.state.player_positions[1 - self.state.current_player][1]
                # 現在のプレイヤーが前進している場合
                if (self.state.current_player == 1 and current_y > previous_y) or \
                    (self.state.current_player == 0 and current_y < previous_y):
                    return 10.0  # 序盤の前進に高い評価を与える
        return 0.0
    
    def expand(self):
        for move in self.state.get_legal_moves(False):
            new_state = self.state.copy()
            new_state.make_move(move)
            child = MCTSNode(new_state, self, move)
            self.children.append(child)

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves(False))


    def best_child(self, c_param=1.4):
        choices_weights = []
        for c in self.children:
            if c.visits > 0:
                early_move_bonus = c.evaluate_early_moves()
                weight = (c.value / c.visits) + early_move_bonus + c_param * math.sqrt((2 * math.log(self.visits) / c.visits))
            else:
                weight = float('inf')  # 未訪問のノードに高い重みを与える
            choices_weights.append(weight)
        return self.children[choices_weights.index(max(choices_weights))]


async def mcts(root, iterations=100):
    for _ in range(iterations):
        node = root
        while node.is_fully_expanded():
            node = node.best_child()

        if not node.is_fully_expanded():
            node.expand()
            node = random.choice(node.children)

        result = await simulate(node.state)

        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    return root.best_child(c_param=0).move

async def simulate(state):
    sim_state = state.copy()
    count = 0
    while not sim_state.is_terminal():
        await asyncio.sleep(0)
        moves = sim_state.get_legal_moves(False)
        _move = None
        count += 1
        if count >= 1000:
            return -1
        for m in moves:
            if len(m) == 3:
                if sim_state.current_player == 0:
                    if m[2] == 8:
                        _move = m
                        break
                else:
                    if m[2] == 0:
                        _move = m
                        break
        if _move:
            move = _move
        else:
            try:
                move = random.choice(moves)
            except:
                print(sim_state.board)
                print(sim_state.player_positions)
                print(moves)
                exit()
        sim_state.make_move(move)
    print(count)
    return sim_state.get_result()


class Mode:
    def __init__(self, board_name="AI Room"):
        self.player = [None, None]
        self.state = QuoridorState()
        self.uids = [None, None]
        self.ws = [None, None]
        self.player_name = [None, None]
        self.board_name = board_name
        self.is_start = False

    def set_ws(self, uid, ws):
        self.ws[self.uids.index(uid)] = ws

    def del_ws(self, uid):
        self.ws[self.uids.index(uid)] = None
        

    def is_del(self):
        if self.player[1] == "ai":
            if self.ws[0] == None:
                return True
            
        count = 0
        for _ws in self.ws:
            if _ws is None:
                count += 1

        if count == 2:
            return True
        return False
    
    async def notify_ws(self, uid = None):
        state = self.state
        board = state.board
        board_name = self.board_name

        for i in range(2):
            ws = self.ws[i]
            if ws is None:
                continue
            _uid = self.uids[i]
            if uid is not None:
                if uid != _uid:
                    continue
            turn = self.is_turn(_uid)
            name = self.player_name[i]
            other_name = self.player_name[1-i]
            position = state.player_positions[i]
            other_position = state.player_positions[1-i]
            wall = state.walls[i]
            other_wall = state.walls[i-1]
            color = self.get_color(i)
            data = {
                    "name": name,
                    "other_name": other_name,
                    "turn": turn,
                    "position": position,
                    "other_position": other_position,
                    "wall": wall,
                    "other_wall": other_wall,
                    "color": color,
                    "board": board,
                    "board_name": board_name
                }
            if turn:
                move_list = state.get_legal_moves_do(i)
                other_move_list = state.get_legal_moves_do(1-i)
                data["move_list"] = move_list
                data["other_move_list"] = other_move_list
            await ws.send_json(data)

    def get_user(self, uid):
        return uid in self.uids

    def is_turn(self, uid):
        return self.state.current_player == self.uids.index(uid)


    def get_color(self, player):
        return "w" if player == 0 else "b"


    def get_ws(self, uid):
        return self.ws[self.uids.index(uid)]

    def set_is_start(self):
        self.is_start = True

    def set_player(self, mode, uid, name=''):
        #mode = 0 player1
        #mode = 1 player2
        #mode = 2 human vs ai
        if mode == 0:
            self.player[0] = "human"
            self.uids[0] = uid
            self.player_name[0] = name
        elif mode == 1:
            self.player[1] = "human"
            self.uids[1] = uid
            self.player_name[1] = name
        elif mode == 2:
            self.player[0] = "human"
            self.player[1] = "ai"
            self.uids[0] = uid
            self.player_name[0] = name
    
    async def win(self, uid):
        for _uid, ws in zip(self.uids, self.ws):
            if _uid == uid:
                await ws.send_json({"message": "勝利!"})
            else:
                await ws.send_json({"message": "敗北..."})

    async def lose(self, uid):
        for _uid, ws in zip(self.uids, self.ws):
            if _uid == uid:
                await ws.send_json({"message": "敗北..."})
            else:
                await ws.send_json({"message": "勝利!"})

        
    async def run(self, uid, move_type, x, y, wall_type=None):
        player1_type = self.player[0]
        state = self.state
        current_uid = self.uids[state.current_player]
        
        if uid == current_uid:
            move = ()   
            if move_type == 'm':
                if ('move', x, y) in state.get_legal_moves():
                    move = ('move', x, y)
                else:
                    return 1 # invalid input
            elif move_type == 'w':
                if ('wall', x, y, wall_type) in state.get_legal_moves():
                    move = ('wall', x, y, wall_type)
                else:
                    return 1 # invalid input
            else:
                return 1
            state.make_move(move)

            return await self.send(uid)
        else:
            return 2 # not turn
    

    async def send(self, uid):
        state = self.state
        if state.get_result() == -1 or state.get_result() == 1:
            await self.win(uid)
            return 3 # win
        else:
            await self.notify_ws()
        return 0 # success


    async def run_ai(self):
        player2_type = self.player[1]
        state = self.state

        if player2_type == "ai":
            root = MCTSNode(state)
            move = await mcts(root)
            state.make_move(move)
        
        await self.send(None)
