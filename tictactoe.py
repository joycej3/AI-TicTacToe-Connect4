
from tkinter import *
import numpy as np
from tictactoe_opponent import max_val, random_pick, QLearning


#Change these values
#.....................................
games_to_be_played = 250000

# playerX = "random"
playerX = "q_learning"

playerO = "random"
# playerO = "minmax"
#.....................................


size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'

alpha = -1000
beta =  1000
WIN_VALUE = 2.0
DRAW_VALUE = 1.0
LOSS_VALUE = -2.0

player_X_code = -1
player_O_code = 1


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        # self.qlearning = QLearning()
        self.q_learning = QLearning()
      

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = ' '
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = ' '
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = ' '
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X): ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie               : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:#
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)


    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = player_X_code if player == 'X' else player_O_code

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        return gameover


    def legal_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board_status[i][j] == 0:
                    flat_index = i * self.board_status.shape[1] + j
                    moves.append(flat_index)

        return moves
    
    def get_reward(self):
        if self.is_winner('X'):
            return 2
        elif self.is_winner('O'):
            
            return -2
        elif self.is_tie():
            return 1
        else:
            return 0
        

    def play(self):
        games_played = 0
        while games_played < games_to_be_played :
        
            if not self.reset_board:
                pos = [-1, -1]
                if self.player_X_turns == True:
                    # pos = self.qlearning.get_action(self)
                    # qlearning resut here
                    if (playerX == "q_learning"):
                        self.q_learning.actions = self.legal_moves()
                        flat_index = self.q_learning.choose_action(self.board_status) 
                        pos[0] = flat_index // 3
                        pos[1] = flat_index % 3
                        self.board_status[pos[0]][pos[1]] = player_X_code    
                        self.draw_X(pos)  
                        #update
                        if self.legal_moves():
                            self.q_learning.actions = self.legal_moves()
                            next_pos = random_pick(self)
                            next_status = self.board_status.copy()
                            next_status[next_pos[0]][next_pos[1]] = player_O_code
                            temp = self.board_status[next_pos[0]][next_pos[1]] 
                            self.board_status[next_pos[0]][next_pos[1]] = player_O_code
                            reward = self.get_reward()
                            self.board_status[next_pos[0]][next_pos[1]] = temp
                            fin =0
                        else:
                            fin =1
                            
                            reward = 0
                        self.q_learning.update(self.board_status, flat_index, reward, next_status, fin)
                    else:
                        pos = random_pick(self)
                        self.board_status[pos[0]][pos[1]] = player_X_code    
                        self.draw_X(pos)  
                    
                else:
                    if playerO == "minmax":
                        (m, pos[0], pos[1]) = max_val(self, alpha, beta) #call minmax
                    else:
                        pos = random_pick(self)
                    # (m, pos[0], pos[1]) = max_val(self, alpha, beta) #call minmax
                    # self.qlearning.update_q_table(self.board_status)
                    self.draw_O(pos)
                    self.board_status[pos[0]][pos[1]] = player_O_code
                    
                self.player_X_turns = not self.player_X_turns

                if self.is_gameover():
                    
                    self.display_gameover()
        
            else:  # Play Again
                games_played = games_played + 1
                print(games_played)
                self.canvas.delete("all")
                self.play_again()
                self.reset_board = False

        
        self.display_gameover()


    def click(self, event):
        self.play()

game_instance = Tic_Tac_Toe()
game_instance.mainloop()