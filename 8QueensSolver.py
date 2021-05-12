import numpy as np
from collections import defaultdict

BLOCKED = -1   #Cell is blocked due to a previously placed queen
OCCUPIED = 1   #Cell is occupied by a queen
AVAILABLE = 0  #CEll is available. Initially all cells are available.

class EightQueensSolver:
  def __init__(self):
    self.board = np.zeros((8,8))
    return
  
  def mark_blocked_cells(self, occupied_cell, board_config):
    already_blocked_cells_count = 0
    x_current = occupied_cell[0]
    y_current = occupied_cell[1]
    
    # Block rows and columns
    for i in range(0, 8):
      if board_config[i, y_current] == BLOCKED:
        already_blocked_cells_count += 1
      if board_config[x_current, i] == BLOCKED:
        already_blocked_cells_count += 1
      
      board_config[i, y_current] = BLOCKED
      board_config[x_current, i] = BLOCKED
    
    x_idx = x_current
    y_idx = y_current
    # Block both diagonals
    for x_ctr in [-1, 1]:
      for y_ctr in [-1, 1]:
        while(-1 < x_idx+x_ctr and x_idx+x_ctr < 8 and -1 < y_idx+y_ctr and y_idx+y_ctr < 8):
          x_idx = x_idx + x_ctr
          y_idx = y_idx + y_ctr

          if board_config[x_idx, y_idx] == BLOCKED: 
            already_blocked_cells_count += 1
          
          board_config[x_idx, y_idx] = BLOCKED
        x_idx = x_current
        y_idx = y_current
    
    board_config[x_current, y_current] = OCCUPIED
    return board_config, already_blocked_cells_count
  

  def get_profits_at_config(self, configuration):
    available_indices = np.where(configuration == AVAILABLE)
    return len(available_indices[0])


  def search_placement_config(self):
    
    # Strategy1: Start by placing Q1 @ (0, 7). This reduces the board to be of size 7x7 without the diagonals.
    self.board[0, 7] = OCCUPIED
    self.mark_blocked_cells((0, 7), self.board)


    # At each level, we pick the next row to assign a place to the queen. We start from 7 and go down to 0. 
    level = 6
    child_idx = 0

    # In each row, we pick the configuration that gives max profit. Profit is defined as max number of free cells available after placing the queen and the maximum number of overlapping blocked cells.
    # For row r, col c, Profit(r, c) = max over_all_c(#available cells, #overlapping blocked cells)

    while level > -1:
      row_col_candidates_at_level = defaultdict(dict)

      for i in range(0, 7):
        current_board = self.board.copy()
        row_id = 7 - level
        if current_board[row_id, i] == AVAILABLE:
          current_board[row_id, i] = OCCUPIED
          current_board, count_overlap_blocked = self.mark_blocked_cells((row_id, i), current_board)
          row_col_candidates_at_level[level][child_idx] =[(self.get_profits_at_config(current_board), current_board, count_overlap_blocked, i)]
          child_idx += 1

      max_profit_move = sorted(row_col_candidates_at_level[level].items(), key=lambda x: (x[1][0][0], x[1][0][2]), reverse=True)
      # max_profit_move_list = [(xpp[1][0][3], xpp[1][0][0], xpp[1][0][2]) for xpp in max_profit_move]
      if len(max_profit_move) > 0:
        max_profit_move = max_profit_move[0]
        self.board = max_profit_move[1][0][1]
      
    #   print("Max profits sorted at level: {}".format(level))
    #   print(max_profit_move_list)
      print("Next config: ")
      print(self.board)
      level = level - 1
    
    while len(np.where(self.board == 1)) < 8 and len(np.where(self.board == AVAILABLE)[0])>0:
      available_pos = np.where(self.board == AVAILABLE)
      cx = available_pos[0][0]
      cy = available_pos[1][0]

      if self.board[cx, cy] == AVAILABLE:
        self.board[cx, cy] = OCCUPIED
        self.board, coverlap = self.mark_blocked_cells((cx, cy), self.board)
      else:
        self.board[cx, cy] == BLOCKED
      print("Next config: \n", self.board)
    
    for i in range(0, 8):
      for j in range(0, 8):
        if self.board[i, j] == BLOCKED:
          self.board[i, j] = 0
    
    print("Final positions of the queens:\n", self.board)
    return


solver = EightQueensSolver()
solver.search_placement_config()
