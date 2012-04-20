# Master Search

# This does a mini-max algorithm, but stores the best 3 options, it then chooses one of these solutions at random with the following probabilities:
# 80% chance of the optimal
# 15% chance of the second best
# 5% chance of the last one
import random
from Queue import PriorityQueue
prob1 = .8
prob2 = .15

def minimax(game, depth=3):
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
      moves = game.valid_moves(colour)[1]
      if len(moves)==0: # if we're at a leaf
        best = "pass"
        value = eval(new,'B')
      elif len(moves) == 1:
        best = moves[0]
        moveset = game.valid_moves(colour)[0]
        new = game.copy()
        new.make_move(moves[0][0],moves[0][1], moveset)
        value = eval(game,'B')
      else:
        for move in moves:
          moveset = game.valid_moves(colour)[0]
          new = game.copy()
          new.make_move(move[0],move[1], moveset)
          temp = min_val(new, level)
          if temp[0] > value:
            value = temp[0]
            best = move
        return [value, best]
    else:
      value = eval1(game, 'B')
      best = [0,0] # just need a dummy value
      return [value, best] # smallest possible heuristic therefore will never be chosen

  def min_val(game, level):
    """ Optimal choice for opponent. Returns the move that the opponent should make in order to minimise the computers heuristic """
    level += 1
    colour = 'B'
    if level <= depth:
      value = won # will never be chosen as we are looking for the min
      best = [0, 0] # just a dummy move
      moves = game.valid_moves(colour)[1]
      if len(moves)==0: # if we're at a leaf
        best = "pass"
        value = eval(new,'B')
      elif len(moves) == 1:
        best = moves[0]
        moveset = game.valid_moves(colour)[0]
        new = game.copy()
        new.make_move(moves[0][0],moves[0][1], moveset)
        value = eval(game,'B')
      else:
        for move in moves:
          moveset = game.valid_moves(colour)[0]
          new = game.copy()
          new.make_move(move[0],move[1], moveset)
          temp = max_val(new, level) # the optimal move and value that computer will make
          if temp[0] < value: # if we have a smaller heuristic option choose it
            value = temp[0]
            best = move
      return [value, best]
    else:
      value = eval1(game, 'B')
      best = [0,0] # just need a dummy value
      return [value, best] #largest possible heuristic therefore will never be chosen

  def eval1(game, colour):
    if colour=="W":
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
  if len(moves) == 0: # no moves possible
    return "pass"
  if len(moves) == 1: # only one possible move
    return moves[0]
  if len(moves) == 2:
    # choose from best two moves with 20% chance of the worse move
    best = minimax(game, depth)
    rand = random.random()
    if random <= .8:
      return best
    else:
      other = moves[0] if moves[1] == best else moves[1]
      return other
  # in this case we store the possible moves in a priority queue (implemented as a heap) Note there is no real optimiisation to this strategy if there are less than 3 moves
  else:
    MyMoves = PriorityQueue()
  for move in moves:
    moveset = game.valid_moves('W')[0]
    new = game.copy()
    new.make_move(move[0],move[1], moveset)
    val = min_val(new, level)
    level = 1
    pq.put(1./val[0],move)
  rand = random.rand()
  best = pq.get()
  if rand > .8:
    best = pq.get()
    if rand > .95:
      best = pq.get()
  return best
  print "Aww yeah I know which move is best I played: ", best
  return best[1]
