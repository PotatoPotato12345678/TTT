import torch
import torch.nn as nn
import random

class TicTacToe():
    def __init__(self, size: int) -> None:
        """Initializes a square Tic-tac-toe field."""
        super().__init__()
        self.size = size
        self.field = torch.zeros(size=(size, size), dtype=torch.long)

    def step(self, action: int, player: int, free_index:list) -> tuple:
        """Performs a single game move for player.

        Args:
            action: The action predicted by the neural network.
            if action is not on available position, takes a random position.

        Returns:
            A tuple holding information about state

        """
        if(action not in free_index):
            action = random.choice(free_index)
        
        x, y = divmod(action, self.size)#index to coordinate
        self.field[x, y] = -1.0
        state = self.field.float()[None, ...]

        return state

    def board_convert(self,board):
        free_index = []
        for i,e in enumerate(board):
            x, y = divmod(i, self.size)
            ne = None
            if e == 'O':
                ne = -1    
            elif e == 'X':
                ne = 1
            elif e == '?':
                ne = 0
                free_index.append(i)
            self.field[x,y] = ne
            state = self.field.float()[None, ...]
        return state,free_index

    def play(self, model: nn.Module, origboard) -> int:
        state,free_index = self.board_convert(origboard)
        action = model.predict(state)
        state = self.step(action=action, player=-1,free_index=free_index)
        """
        print("-----------------")
        print(state,action)
        print("-----------------")
        """
        return action