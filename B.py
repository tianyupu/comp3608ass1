# alpha-beta search
import util

possible = valid_moves()
optimal = []
# need to add evaluation function

# start by doing basic minimax
# but add in additional checks to allow break points i.e. pruning
def alpha_beta(board, game):
  level = 1
  def max_val(board, alpha, beta):
    level = level + 1
    if # game has ended with computer winning:
      return won
    if level <= depth:
      value = lost
      for (a,s) in valid_moves():
        value = max(v,min_val(s, alpha, beta))
        if value >= beta:
          return value
        alpha = max(alpha, value)
      return value
    else:
      break

  def min_val(board):
    level = level + 1
    if # game has ended with computer losing:
      return lost
    if level <= depth:
      value = won
      for (a,s) in valid_moves():
        value = min(v,max_value(s, alpha, beta))
        if value <= alpha:
          return value
        beta = min(beta, value)
      return v
    else:
      break

  a,s = argmax(valid_moves(), lambda ((ac,st)): min_value(st))
  return a
