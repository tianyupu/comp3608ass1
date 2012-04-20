# Minimax Algorithm
import util
import random
won = 10000
lost = -10000

def minimax(game, depth=3,colour='W'):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3
  Colour is the colour the computer is playing"""
  def max_val(game, colour, level):
    level += 1
    othercol = 'W' if colour == 'B' else 'B'
    if level <= depth:
      value = lost
      for move in game.valid_moves('B')[1]:
        value = max(value,min_val(eval1(move,colour)[0]), level)
      return value
    else:
      return lost #smallest possible heuristic therefore will never be chosen

  def min_val(game, colour, level):
    level += 1
    othercol = 'W' if colour == 'B' else 'B'
    if level <= depth:
      value = won
      for move in game.valid_moves('W')[1]:
        value = min(value,max_val(eval1(game, move[0], move[1],othercol)[1]), level)
      return value
    else:
      return won #largest possible heuristic therefore will never be chosen

  def eval1(game, x, y, which):
    new = game.make_move(move[0],move[1],which)
    if which=="white":
      return new.board.get_white()
    else: return new.board.get_black()

  def eval2(move, colour):
    new = game.make_move(move[0],move[1],colour)
    heur = 0
    # for each token multiply it by stability and add them up
    toks = new.board.get_alltoks()
    for tok in toks:
      if tok.get_colour() == colour:
        heur += tok.stability()
    # add twice the number of possible moves
    heur += 2*len(new.valid_moves)

  # body of minimax
  level = 1
  moves = game.valid_moves('W')[1]
  best = [moves[0],0]
  for move in moves:
    val = min_val(game, 'B', level)
    level = 1
    if val[1] > best[1]:
      best = val
  return best[0]
  # a,s = argmax(valid_moves(), lambda ((ac,board)): min_value(board))
  return a
