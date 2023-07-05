
# from numpy import random
from collections import defaultdict
import numpy as np

player_X_code = -1
player_O_code = 1

def smart_move(self):
    move = [-1,-1]
    lose_val = -2 + (int(self.player_X_turns) * 4)
    win_val = 2 + (int(self.player_X_turns) * -4)

    for i in range(3):
        if self.board_status[i][0] + self.board_status[i][1] + self.board_status[i][2] == win_val:
            for j in range(3):
                if self.board_status[i][j] == 0:
                    return [i, j]
        elif  self.board_status[0][i] + self.board_status[1][i] + self.board_status[2][i] == win_val:
           for j in range(3):
                if self.board_status[j][i] == 0:
                    return [j, i]   
                         
    if  self.board_status[0][0] + self.board_status[1][1] + self.board_status[2][2] == win_val:
        for j in range(3):
                if self.board_status[j][j] == 0:
                    return [j, j]
    elif  self.board_status[0][2] + self.board_status[1][1] + self.board_status[2][0] == win_val:
        for j in range(3):
                if self.board_status[j][2-j] == 0:
                    return [j, 2-j]

    for i in range(3):
        if self.board_status[i][0] + self.board_status[i][1] + self.board_status[i][2] == lose_val:
            for j in range(3):
                if self.board_status[i][j] == 0:
                    return [i, j]
        elif  self.board_status[0][i] + self.board_status[1][i] + self.board_status[2][i] == lose_val:
           for j in range(3):
                if self.board_status[j][i] == 0:
                    return [j, i]           
    if  self.board_status[0][0] + self.board_status[1][1] + self.board_status[2][2] == lose_val:
        for j in range(3):
                if self.board_status[j][j] == 0:
                    return [j, j]
    elif  self.board_status[0][2] + self.board_status[1][1] + self.board_status[2][0] == lose_val:
        for j in range(3):
                if self.board_status[j][2-j] == 0:
                    return [j, 2-j]
    return move
def random_pick(self):
    logical_position = smart_move(self) 

    if logical_position == [-1, -1]:
        logical_position = np.random.randint(3, size=(2)) 
        while self.is_grid_occupied(logical_position):
            # print(self.board_status)
            logical_position = np.random.randint(3, size=(2)) 

    return logical_position


def max_val(self, alpha, beta):

    maxv = -2
    pos = [-1, -1]

    
    if self.is_gameover():
        if self.X_wins:
            return (player_X_code, 0, 0)
        if self.O_wins:
            return (player_O_code, 0, 0)
        if self.tie:
            return (0, 0, 0)
        
    for i in range(3):
        for j in range(3):
            if self.board_status[i][j] == 0:

                self.board_status[i][j] = player_O_code
                (m, min_i, min_j) = min_val(self, alpha, beta)
            
                if m > maxv:
                    maxv = m
                    pos[0] = i
                    pos[1] = j
             
                self.board_status[i][j] = 0
                if maxv >= beta:
                    return (maxv, pos[0], pos[1])
                alpha = max(alpha, maxv)
    return (maxv, pos[0], pos[1])
def min_val(self, alpha, beta):
    minv = 2
    pos = [-1, -1]

    if self.is_gameover():
        if self.X_wins:
            return (player_X_code, 0, 0)
        if self.O_wins:
            return (player_O_code, 0, 0)
        if self.tie:
            return (0, 0, 0)

    for i in range(0, 3):
        for j in range(0, 3):
            if self.board_status[i][j] == 0:
                self.board_status[i][j] = player_X_code
                (m, max_i, max_j) = max_val(self,alpha, beta)
                if m < minv:
                    minv = m
                    pos[0] = i
                    pos[1] = j
                self.board_status[i][j] = 0
                if minv <= alpha:
                    return (minv, pos[0], pos[1])
                beta = min(beta, minv)

    return (minv, pos[0], pos[1])

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q ={}
        self.actions  = None
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.board = np.zeros(shape=(3, 3))
        self.size = 3

    def update(self, state, action, reward, next_state, fin):
        # if( reward != 0): 
            # print(reward)
        if fin == 1:
            # print(reward)
            return
        flat_state = tuple(state.flatten())
        flat_next_state = tuple(next_state.flatten())
        if flat_state not in self.q:
            self.q[flat_state] = np.zeros(shape=(3, 3))
        
        if flat_next_state not in self.q:
            self.q[flat_next_state] = np.zeros(shape=(3, 3))

        flat_index = self.choose_action(next_state)

        pos = [ flat_index // self.size,  flat_index % self.size]
        td_target = reward + self.gamma * self.q[flat_next_state][pos[0]][pos[1]]
        

        pos = [action // self.size, action % self.size]
        td_error = td_target - self.q[flat_state][pos[0]][pos[1]]
        self.q[flat_state][pos[0]][pos[1]] += self.alpha * td_error



 
    def choose_action(self, state):

        flat_state = tuple(state.flatten())
        
        if flat_state not in self.q:
            self.q[flat_state] = np.zeros(shape=(3, 3))
            return np.random.choice(self.actions)
           
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.actions)
        else:
        
            return np.argmax(self.q[flat_state])

    