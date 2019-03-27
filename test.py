from copy import deepcopy 

xdim, ydim = 3, 2

class GameState:

    def __init__(self):
        self.board = [[0 for x in range(xdim)] for y in range(ydim)] 
        self.board[-1][-1] = 1
        self.whose_turn = 0
        self.player_locations = [None, None]
        
    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.
        
        
        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        if move not in get_legal_moves(self):
            raise RuntimeError("Attempted forecast of illegal move")
        newGameState = deepcopy(self)
        newGameState[move[0]][move[1]] = 1
        newGameState.player_locations[whose_turn] = move
        newGameState.whose_turn ^= 1
        return newGameState
  
    
    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        moves = []
        if self.player_locations[self.whose_turn] is None:
            return self.get_blank_locations()
        matrix = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1, 1), (-1,-1)]

        for dx, dy in matrix:
            x,y = self.player_locations[self.whose_turn]
            while x+dx <= xdim and x+dx >= 0 and y+dy <= ydim and y+dy >= 0:
               x = x+dx
               y = y+dx
               if self.board[x][y] : break
               moves.append((x,y))
        return moves    
        
    def get_blank_locations(self):
        print("\n\n\n\n#######\n\n")
        for y in range(ydim): print(y)
        print("\n\n\n\n#######\n\n")

        return [(x,y) for y in range(ydim) for x in range(xdim)
        if (self.board[x][y] == 0)]
   


print("Creating empty game board...")
g = GameState()

print("Getting legal moves for player 1...")
p1_empty_moves = g.get_legal_moves()
print("Found {} legal moves.".format(len(p1_empty_moves or [])))

print("Applying move (0, 0) for player 1...")
g1 = g.forecast_move((0, 0))

print("Getting legal moves for player 2...")
p2_empty_moves = g1.get_legal_moves()
if (0, 0) in set(p2_empty_moves):
    print("Failed\n  Uh oh! (0, 0) was not blocked properly when " +
          "player 1 moved there.")
else:
    print("Everything looks good!") 
