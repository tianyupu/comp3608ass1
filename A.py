# Minimax Algorithm
import util

def minimax(board, game, depth=3):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3"""
  level = 1
  def max_val(board):
    level = level + 1
    if level <= depth:
      value = lost
      for move in valid_moves():
        value = max(value,min_val(eval1(move)[0]))
      return value
    else:
      return lost #smallest possible heuristic therefore will never be chosen

  def min_val(board):
    level = level + 1
    if level <= depth:
      value = won
      for move in valid_moves():
        value = min(value,max_value(eval1(move)[1]))
      return value
    else:
      return won #largest possible heuristic therefore will never be chosen

  a,s = argmax(valid_moves(), lambda ((ac,board)): min_value(board))
  return a
