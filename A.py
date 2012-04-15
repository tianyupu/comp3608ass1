# Minimax Algorithm
import util

# need to add evaluation function

def minimax(board, game, depth=3):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3"""
  level = 1
  def max_val(board):
    level = level + 1
    if # game has ended with computer winning:
      return won
    if level <= depth:
      value = lost
      for (a,s) in valid_moves():
        value = max(v,min_val(s))
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
        value = min(v,max_value(s))
      return v
    else:
      break

  a,s = argmax(valid_moves(), lambda ((ac,st)): min_value(st))
  return a
