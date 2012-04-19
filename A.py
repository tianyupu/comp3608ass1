# Minimax Algorithm
import util

def minimax(board, game, depth=3,colour):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3
  Colour is the colour the computer is playing"""
  level = 1
  def max_val(board, colour):
    level = level + 1
    if level <= depth:
      value = lost
      for move in valid_moves():
        value = max(value,min_val(eval1(move,colour)[0]))
      return value
    else:
      return lost #smallest possible heuristic therefore will never be chosen

  def min_val(board, colour):
    level = level + 1
    if colour == black:
      othercol = white
    else:
      othercol = black
    if level <= depth:
      value = won
      for move in valid_moves():
        value = min(value,max_value(eval1(move,othercol)[1]))
      return value
    else:
      return won #largest possible heuristic therefore will never be chosen

  def eval1(move, which):
    new = game.make_move(move)
    if which=="white":
      return new.board.get_white()
    else return new.board.get_black()

  def eval2(move, colour):
    new = game.make_move(move)
    heur = 0
    # for each token multiply it by stability and add them up
    toks = new.board.get_alltoks()
    for tok in toks:
      if tok.get_colour() == colour:
        heur += tok.stability()
    # add twice the number of possible moves
    heur += 2*len(new.valid_moves)
  a,s = argmax(valid_moves(), lambda ((ac,board)): min_value(board))
  return a
