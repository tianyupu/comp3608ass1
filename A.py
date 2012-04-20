# Minimax Algorithm
import util
won = 10000
lost = -10000
import copy

def minimax(game, depth=3,colour='W'):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3
  Colour is the colour the computer is playing"""
  def max_val(game, level):
    level += 1
    colour = 'W'
    # need to explore deeper nodes
    if level <= depth:
      value = lost
      for move in game.valid_moves(colour)[1]:
        moveset = game.valid_moves(colour)[0]
        new = game.copy()
        new.make_move(move[0],move[1], moveset)
        temp = min_val(new, 'B', level)
        if value < temp:
          value = temp
          best = move
      return value
    else:
      value = eval1(game, 'B')
      return value #smallest possible heuristic therefore will never be chosen

  def min_val(game, level):
    level += 1
    colour = 'B'
    if level <= depth:
      value = won
      for move in game.valid_moves(colour)[1]:
        moveset = game.valid_moves(colour)[0]
        new = game.copy()
        new.make_move(move[0],move[1], moveset)
        temp = max_val(new, level)
        if value < temp:
          value = temp
          best = move
      return value
    else:
      value = eval1(game, 'B')
      return value #largest possible heuristic therefore will never be chosen

  def eval1(game, colour):
    if which=="colour":
      return game.board.get_white()
    else:
      return game.board.get_black()

  def eval2(move, colour):
    moveset = game.valid_moves(which)[0]
    new = game.make_move(move[0],move[1], moveset)
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
    moveset = game.valid_moves(colour)[0]
    new = game.copy()
    new.make_move(move[0],move[1], moveset)
    val = min_val(new, level)
    level = 1
    if val[1] > best[1]:
      best = val
  return best[0]
  # a,s = argmax(valid_moves(), lambda ((ac,board)): min_value(board))
  return a
