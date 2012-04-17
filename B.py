# alpha-beta search
import util

# start by doing basic minimax
# but add in additional checks to allow break points i.e. pruning
def alpha_beta(board, game, alpha, beta, depth):
  level = 1
  def max_val(board, alpha, beta):
    level = level + 1
    if level <= depth:
      value = lost
      for move in valid_moves():
        value = max(value,min_val(eval1(move), alpha, beta))
        if value >= beta:
          return value
        alpha = max(alpha, value)
      return value
    else:
      return lost #smallest possible heuristic therefore will never be chosen

  def min_val(board):
    level = level + 1
    if level <= depth:
      value = won
      for move in valid_moves():
        value = min(value, max_value(eval1(move), alpha, beta))
        if value <= alpha:
          return value
        beta = min(beta, value)
      return value
    else:
      return won #largest possible heuristic therefore will never be chosen

  a,s = argmax(valid_moves(), lambda ((ac,board)): min_value(board))
  return a
