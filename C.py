# Master Search

# This does a mini-max algorithm, but stores the best 3 options, it then chooses one of these solutions at random with the following probabilities:
# 80% chance of the optimal
# 15% chance of the second best
# 5% chance of the last one
import random
import A
won = 10000
lost = -10000
from Queue import PriorityQueue
prob1 = .8
prob2 = .15

def master(game):
  """ Given a game and the current board it should go to level depth to determine which move to make. Default depth is 3
  Colour is the colour the computer is playing"""
  def max_val(game, level):
    """ Optimal choice for computer. Returns the move that the computer should make in order to maximise its heuristic value """
    level += 1
    colour = 'W'
    # need to explore deeper nodes
    if level <= depth:
      value = lost # should never be chosen
      best = [0, 0] # just a dummy move
      moves = game.valid_moves(colour).keys()#[1]
      if len(moves)==0: # if we're at a leaf
        best = "pass"
        value = min_val(game, level)
      elif len(moves) == 1:
        best = moves[0]
        moveset = game.valid_moves(colour)#[0]
        new = game.copy()
        new.make_move(moves[0][0],moves[0][1], moveset)
        value = min_val(new, level)
      else:
        for move in moves:
          moveset = game.valid_moves(colour)#[0]
          new = game.copy()
          new.make_move(move[0],move[1], moveset)
          temp = min_val(new, level)
          if temp[0] > value:
            value = temp[0]
            best = move
      return [value, best]
    else:
      value = eval2(game, 'W')
      best = [0,0] # just need a dummy value
      return [value, best] # smallest possible heuristic therefore will never be chosen

  def min_val(game, level):
    """ Optimal choice for opponent. Returns the move that the opponent should make in order to minimise the computers heuristic """
    level += 1
    colour = 'B'
    if level <= depth:
      value = won # will never be chosen as we are looking for the min
      best = [0, 0] # just a dummy move
      moves = game.valid_moves(colour).keys()#[1]
      if len(moves)==0: # if we're at a leaf
        best = "pass"
        value = max_val(game, level)
      elif len(moves) == 1:
        best = moves[0]
        new = game.copy()
        moveset = new.valid_moves(colour)#[0]
        new.make_move(moves[0][0],moves[0][1], moveset)
        value = max_val(new, level)
      else:
        for move in moves:
          new = game.copy()
          moveset = new.valid_moves(colour)#[0]
          new.make_move(move[0],move[1], moveset)
          temp = max_val(new, level) # the optimal move and value that computer will make
          if temp[0] < value: # if we have a smaller heuristic option choose it
            value = temp[0]
            best = move
      return [value, best]
    else:
      value = eval2(game, 'W')
      best = [0,0] # just need a dummy value
      return [value, best] #largest possible heuristic therefore will never be chosen

  def eval1(game, colour):
    if colour=="W":
      return game.board.get_white()
    else:
      return game.board.get_black()

  def eval2(game, colour):
    heur = 0
    # for each token multiply it by stability and add them up
    toks = game.board.get_alltoks()
    for tok in toks:
      if tok.get_colour() == colour:
        heur += tok.get_stability()*2
    # add twice the number of possible moves
    heur += len(new.valid_moves(colour))
    return heur

  # MINIMAX BODY
  # global vars
  level = 1
  depth = 3
  moves = game.valid_moves('W').keys()
  if len(moves) == 0: # no moves possible
    return "pass" # this should never be run because it should be found in premove
  elif len(moves) == 1: # only one possible move
    return moves[0]
  elif len(moves) == 2:
    # choose from best two moves with 20% chance of the worse move
    best = A.minimax(game)
    rand = random.random()
    if rand <= .8:
      return best
    else:
      other = moves[0] if moves[1] == best else moves[1]
      return other
  # in this case we store the possible moves in a priority queue (implemented as a heap) Note there is no real optimiisation to this strategy if there are less than 3 moves
  else:
    sortlist = []
    for move in moves:
      new = game.copy()
      moveset = new.valid_moves('W')
      new.make_move(move[0],move[1], moveset)
      val = min_val(new, level)
      level = 1
      sortlist.append([val[0],move])
    rand = random.random()
    sortlist.sort()
    #best = pq.get()
    best = sortlist.pop()
    if rand > .8:
      best = sortlist.pop()
      if rand > .95:
        best = sortlist.pop()
    print "Aww yeah I know which move is best I played: ", best
    return best[1]
