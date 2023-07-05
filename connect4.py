import numpy as np
import random
import pygame
import sys
import math
from connect4_opponent import minimax, smart_random, QLearning
# from connect4_opponent import  minimax

#Change these values
#.....................................
games_to_be_played = 1000

# player1_strat = "random"
player1_strat = "q_learning"

# player2_strat = "random"
player2_strat = "minmax"
#.....................................
WINNING_REWARD = 1
LOSING_REWARD = -1


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = -1
WINDOW_LENGTH = 4

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

games = 0
player1_wins = 0
player2_wins = 0
alpha = -math.inf
beta =  math.inf
q_learning = QLearning()

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
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


while games < games_to_be_played:
    moves = 0
    board = create_board()
    game_over = False
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 75)
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    turn = random.randint(PLAYER, AI)

    while not game_over:
        reward = 0.01
        if turn == PLAYER and not game_over:
            if player1_strat == "q_learning":

                actions = []
                for c in range(COLUMN_COUNT):
                    if is_valid_location(board, c):
                        actions.append(c)
                col = q_learning.choose_action(board, actions)
                
                
            else:
                col = smart_random(board, PLAYER_PIECE)
        
            if is_valid_location(board, col):
                turn += 1
                turn = turn % 2
                moves = moves + 1
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    player1_wins = player1_wins + 1
                    screen.blit(label, (40,10))
                    game_over = True
                    reward = WINNING_REWARD

                if player1_strat == "q_learning":
                    #update
                    if moves != (ROW_COUNT * COLUMN_COUNT) - 1:
                        

                        next_col = smart_random(board, AI_PIECE)
                        next_row = get_next_open_row(board, next_col)
                        next_board = board.copy()
                        next_board[next_row][next_col] = AI_PIECE
                        actions = []
                        for c in range(COLUMN_COUNT):
                            if is_valid_location(board, c):
                                actions.append(c)

                        temp = board[next_row][next_col] 
                        board[next_row][next_col] = AI_PIECE
                        
                        if reward == 0.01 and winning_move(board, AI_PIECE):
                            reward = -1
                        
                        board[next_row][next_col] = temp
                        fin =0
                        
                    else:
                        fin =1
                        reward = 0
                    q_learning.update(board,row, col, actions, reward, next_board, fin)

                draw_board(board)
                # pygame.time.wait(1000)
                if moves >= ROW_COUNT * COLUMN_COUNT: 
                    print("test")
                    pygame.time.wait(1000)
                    game_over = True

                
        
        # # Ask for Player 2 Input
        if turn == AI and not game_over:				
            if player2_strat == "minmax":
                col, minmax_score = minimax(board, 5, alpha, beta, True)
                
            else:
                col = smart_random(board, AI_PIECE)
            # col = random.randint(0, COLUMN_COUNT-1)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    player2_wins = player2_wins + 1
                    screen.blit(label, (40,10))
                    game_over = True
                draw_board(board)
                turn += 1
                turn = turn % 2
                moves = moves + 1
                if moves >= ROW_COUNT * COLUMN_COUNT - 1:
                    print(moves) 
                    # pygame.time.wait(1000)
                    game_over = True

        if game_over:
            games = games + 1
            
            # pygame.time.wait(1000)
    print("Player 1 wins: ", player1_wins)
    print("PLayer 2 wins: ", player2_wins)
     