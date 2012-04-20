#!/usr/bin/python

class Node(object):
  def __init__(self, game, depth, colour, x, y, moveset):
    """Creates a node containing the state of the game if the move of (x, y)
    with colour 'colour' had been made, then generates all the children --
    all possible moves the opposing player could have made in response to this
    particular move."""
    self.game = game.copy()
    self.game.make_move(x, y, moveset) # makes the move
    self.depth = depth
    self.colour = colour
    self.other_col = 'B' if colour == 'W' else 'W'
    self.children = []
    moves = self.game.valid_moves(self.other_col)[0] # [0] for the moveset of all opponent responses
    for move in moves:
      new = self.game.copy()
      nx, ny = move[0], move[1]
      new.make_move(nx, ny, move)
      self.children.append(new)
  def eval_1(self, colour):
    if colour == "W":
      return self.game.board.get_white()
    else:
      return self.game.board.get_black()
  def eval_2(self, move, colour): # not used currently
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
  def get_game(self):
    return self.game
  def get_children(self):
    return self.children
  def get_depth(self):
    return self.depth
  def get_colour(self):
    return self.colour

def minimax(node, depth):
  if len(node.get_children()) == 0 or depth <= 0:
    return node.eval_1('W')
  alpha = -1000000
  for child in node.get_children():
    alpha = max(alpha, -minimax(child, depth-1))
  return alpha