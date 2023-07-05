import numpy as np
import random
import pygame
import sys
import math


# from connect4 import 

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# PLAYER = 0
# AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = -1

WINDOW_LENGTH = 4

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0



def smart_move(board, piece):
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            r = get_next_open_row(board, c)
            temp = board[r][c]
            board[r][c] = piece
            if winning_move(board, piece):
                board[r][c] = temp
                return c
            board[r][c] = temp
    return - 1
def smart_random(board, piece):
    col = smart_move(board, piece)
    if col == - 1:
        col = smart_move(board, -piece)

    if col == - 1:
        col = random.randint(0, COLUMN_COUNT-1)
        while is_valid_location(board, col) ==False:
            col = random.randint(0, COLUMN_COUNT-1)
    
    return col


class QLearning:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.q ={}
        self.actions  = None
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.board = np.zeros(shape=(ROW_COUNT, COLUMN_COUNT))

    def update(self, state, row,col, available_action, reward, next_state, fin):
        if fin == 1:
            return

        flat_state = tuple(state.flatten())
        flat_next_state = tuple(next_state.flatten())
        
        if flat_state not in self.q:
            self.q[flat_state] = np.zeros(shape=( ROW_COUNT, COLUMN_COUNT))
        if flat_next_state not in self.q:
            self.q[flat_next_state] = np.zeros(shape=(ROW_COUNT, COLUMN_COUNT))
        


        # pos = [ flat_index // self.size,  flat_index % self.size]
        col_index = self.choose_action(next_state, available_action)
        row_index = get_next_open_row(state, col_index)
        
        td_target = reward + self.gamma * self.q[flat_next_state][row_index][col_index]
        # pos = [action // self.size, action % self.size]
        col_index = col
        row_index = row

        
        td_error = td_target - self.q[flat_state][row_index][col_index]
        self.q[flat_state][row_index][col_index] += self.alpha * td_error

 
    def choose_action(self, state, act):
        

        flat_state = tuple(state.flatten())
        
        if flat_state not in self.q:
            self.q[flat_state] = np.zeros(shape=(ROW_COUNT, COLUMN_COUNT))
            
            return np.random.choice(act)
           
        if np.random.uniform(0, 1) < self.epsilon:
    
            return np.random.choice(act)
        else:            
            max_index = np.argmax(self.q[flat_state][:, act], axis=None) # Find the index of the maximum value only considering the columns in the 'actions' array
            max_row, max_col = np.unravel_index(max_index, self.q[flat_state][:, act].shape) # Convert the flattened index to row and column indices
            max_col = act[max_col] 

            
            return max_col

    

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, math.inf)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -math.inf)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
