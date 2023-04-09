from collections import deque
from copy import deepcopy

class SudokuBoard:
    def __init__(self, init_board=None):
        values = list(range(1,10))

        if init_board is not None:
            self.board = [[[init_board[y][x]] if init_board[y][x] in values else list(range(1, 10)) for x in range(9)] for y in range(9)]
            for y in range(9):
                for x in range(9):
                    if init_board[y][x] in values:
                        self.wave_function_collapse(self.board, x, y, init_board[y][x])
        else:
            self.board = [[list(range(1, 10)) for x in range(9)] for y in range(9)]

        self.stack = deque()
        self.stack.append(deepcopy(self.board))

    def wave_function_collapse(self, board, x, y, value):
        for i in range(9):
            if (i != x) and value in board[y][i]:
                board[y][i].remove(value)
            if (i != y) and value in board[i][x]:
                board[i][x].remove(value)
        
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        xr = x%3
        yr = y%3

        for i in range(3):
            for j in range(3):
                if (i != yr or j != xr) and value in board[y0 + i][x0 + j]:
                    board[y0 + i][x0 + j].remove(value)

    def is_solved(self, board):
        for y in range(9):
            for x in range(9):
                if len(board[y][x]) > 1:
                    return False
        return True
    
    def is_valid(self, board):
        for y in range(9):
            for x in range(9):
                if len(board[y][x]) == 0:
                    return False
        return True
    
    def find_next_cell(self, board):
        minimum = 10
        x, y = None, None

        for i in range(9):
            for j in range(9):
                if len(board[i][j]) < minimum and len(board[i][j]) > 1:
                    minimum = len(board[i][j])
                    x, y = j, i
                
        return x, y

    def solve(self):
        while len(self.stack) > 0:
            board = self.stack.pop() # get the last board
            if self.is_solved(board):
                return board

            if not self.is_valid(board):
                continue

            x, y = self.find_next_cell(board)
            for value in board[y][x]:
                new_board = deepcopy(board)
                new_board[y][x] = [value]
                self.wave_function_collapse(new_board, x, y, value)
                self.stack.append(new_board)

        return None

init_board = [[None for i in range(9)] for j in range(9)]
init_board[0] = [None, None, None, None, None, 4, None, None, None]
init_board[1] = [None, 9, 8, None, None, None, None, None, None]
init_board[2] = [None, None, 3, None, 2, 8, 7, 4, 1]
init_board[3] = [None, 7, 9, None, None, None, None, None, None]
init_board[4] = [None, None, None, None, 3, None, None, None, None]
init_board[5] = [None, None, None, None, None, None, 6, 5, None]
init_board[6] = [6, 2, 1, 4, 9, None, 3, None, None]
init_board[7] = [None, None, None, None, None, None, 4,7, None]
init_board[8] = [None, None, None, 6, None, None, None, None, None]
SudokuBoard(init_board).solve()