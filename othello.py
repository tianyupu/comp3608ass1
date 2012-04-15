#!/usr/bin/python

import sys

class Token(object):
  def __init__(self, x, y, colour=' ', stability=1):
    """Create a new token.
    
    Arguments:
    x -- the x-coordinate of the token, indicating the row it's in
    y -- the y-coordinate of the token, indicating the column it's in
    colour -- the colour of the token, can be 'B', 'W' or ' '
    stability -- the stability of the token
    """
    self.x = x
    self.y = y
    self.colour = colour
    self.stability = 1 # weighting of stability that the token currently has
  def flip(self):
    """Flips the current colour of the token.
    Only works on tokens that are not blank.
    """
    if self.colour == 'B':
      self.colour = 'W'
    else:
      self.colour = 'B'
  def stabilise(st): # not used currently
    """Used to assess the stability of a token, this is used in the heuristic """
    self.stability = st
  def __str__(self):
    return self.colour
  def __repr__(self):
    return '(%s, %s, %s)' % (self.colour, self.x, self.y)
  def get_colour(self):
    return self.colour
  def get_x(self):
    return self.x
  def get_y(self):
    return self.y
  def __eq__(self, other):
    if other.get_x() == self.x and other.get_y() == self.y and other.get_colour == self.colour:
      return True
    return False
  def __ne__(self, other):
    if other.get_x() != self.x or other.get_y() != self.y or other.get_colour != self.colour:
      return True
    return False

class Board(object):
  """ Defines the board on which the game is played """
  def __init__(self, size):
    self.size = size
    self.tokens = []
    # initialise the board grid with empty tokens
    for i in xrange(size):
      temp = []
      for j in xrange(size):
        # populate the starting tokens
        if (i == size/2-1 and j == size/2-1) or (i == size/2 and j == size/2):
          temp.append(Token(j,i,'W'))
          continue
        if (i == size/2-1 and j == size/2) or (i == size/2 and j == size/2-1):
          temp.append(Token(j,i,'B'))
          continue
        temp.append(Token(j,i))
      self.tokens.append(temp)
  def __str__(self):
    """ return a pretty string representation of the board that can be printed """
    topborder = '+%s+' % ('-' * self.size)
    boardgrid = [topborder]
    for i in xrange(self.size):
      row = '|' + ''.join([t.get_colour() for t in self.tokens[i]]) + '|'
      boardgrid.append(row)
    boardgrid.append(topborder)
    boardstr = '\n'.join(boardgrid)
    return boardstr
  def update(self, x, y):
    # TIAN I'M NOT SURE ABOUT THIS EG. WHAT IF WE ARE ADDING A TOKEN
    # Yes you are absolutely correct -- I haven't implemented it yet :(
    self.tokens[y][x].flip()
  def get_size(self):
    return self.size
  def get_token(self, x, y):
    """Get the token in the board at a particular coordinate indicated by (x, y).
    If the index is out of bounds, return None.
    """
    if x < 0 or x > self.get_size()-1 or y < 0 or y > self.get_size()-1:
      return None
    return self.tokens[y][x]
  def get_adjacent(self, x, y):
    """Returns a list of the 8 tokens surrounding the token located at (x, y).
    If no tokens exist because the coordinates are off the board, then one or
    more Nones will appear in the resulting list.
    """
    toks = [self.get_token(x,y-1), self.get_token(x,y+1), self.get_token(x-1,y), self.get_token(x+1,y), self.get_token(x-1,y-1), self.get_token(x-1,y+1), self.get_token(x+1,y-1), self.get_token(x+1,y+1)] # TIAN I ADDED THE DIAGONALS, THE ASSIGNMENT DESCRIPTION ASKS FOR THEM
    return toks
  def get_alltoks(self):
    """Return a list of all tokens on the board as a one-dimensional list."""
    toks = []
    for i in xrange(self.size):
      for j in xrange(self.size):
        toks.append(self.tokens[j][i])
    return toks
  def get_row(self, y):
    """Returns a row of the board as a list, given the y-coordinate, or None if the
    row does not exist.
    """
    if y < 0 or y > self.get_size()-1:
      return None
    return self.tokens[y]
  def get_column(self, x):
    if x < 0 or y > self.get_size()-1:
      return None
    toks = []
    for i in xrange(self.get_size()):
      toks.append(self.tokens[i][x])
    return toks
# def get_forward_diag(self, x, y):
#   if x < 0 or y > self.get_size()-1 or y < 0 or y > self.get_size()-1:
#     return None
#   toks = []
#   diff = y-x
#   for i in xrange(self.get_size()):
#     toks.append(self.tokens[i][i+diff] # NEED TO DOUBLE CHECK THIS
#   return toks
# def get_backward_diag(self, x, y):
#   if x < 0 or y > self.get_size()-1 or y < 0 or y > self.get_size()-1:
#     return None
#   toks = []
#   diff = y-x
#   for i in xrange(self.get_size()):
#     toks.append(self.tokens[i+diff][i] # NEED TO DOUBLE CHECK THIS
#   return toks


class Player(object):
  """ Defines a player """
  def __init__(self, name, colour):
    self.name = name
    if colour in 'BW':
      self.colour = colour
  def get_name(self):
    return self.name
  def get_colour(self):
    return self.colour

class Game(object):
  def __init__(self, size=8, difficulty=0):
    """Creates a new Othello game.

    Arguments:
    size -- the desired size of the Othello board (default 8)
    difficulty -- the desired difficulty of the computer opponent (default 0). This affects the depth of the search space in the mini-max algorithm etc.
    """
    self.size = size
    self.difficulty = difficulty
    self.board = Board(size)
    self.players = [Player(raw_input("Black player please type your name\n"),'B'), Player(raw_input("White player please type your name\n"), 'W')]
    self.curr_player = 0
  def get_currplayername(self):
    return self.players[self.curr_player].get_name()
  def get_currplayercolr(self):
    return self.players[self.curr_player].get_colour()
  def get_move(self):
    """Gets a move from the player in the form (x, y).

    Assume well-formed input for now.
    """
    line = raw_input("Type your move in the form 'x, y'\n").strip()
    x, y = line.split()
    return int(x), int(y)
  def make_move(self, x, y):
    self.curr_player = int(not self.curr_player) # flip the player
    self.is_valid(self.board.get_token(x,y), self.get_currplayercolr(), update=True)
  def valid_moves(self, colour):
    moves = set()
    other_col = 'W' if colour == 'B' else 'B'
    for tok in self.board.get_alltoks():
      if tok.get_colour() == other_col: # if the colour of the token is of the opposing side,
        adj = self.board.get_adjacent(tok.get_x(), tok.get_y()) # get all its adjacent tokens
        for adjtoken in adj:
          if adjtoken is not None and adjtoken.get_colour() == ' ': # if any of these adjacent tokens are blank,
            moves.add(adjtoken) # then it's a possible place to put our next token
    for move in list(moves):
      if not self.is_valid(move, colour):
        moves.remove(move)
    return list(moves)
  def is_valid(self, token, colour, update=False):
    if self.check_row(token, colour, update) or self.check_col(token, colour, update) or self.check_diag(token, colour, update):
      return True
  def check_row(self, token, colour, update=False):
    tx = token.get_x()
    ty = token.get_y()
    left, right = None, None
    x = tx - 1
    while x >= 0: # scan to the left of the token to find a left flank
      currtok = self.board.get_token(x, ty)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        left = x # set the x-coord of the leftmost flank
      else:
        if update:
          self.board.update(x, ty)
      x -= 1
    x = tx + 1
    while x < self.board.get_size(): # scan to the right of the token to find a right flank
      currtok = self.board.get_token(x, ty)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        right = x # set the x-coord of the leftmost flank
      else:
        if update:
          self.board.update(x, ty)
      x += 1
    if left is None and right is None:
      return False
    return True
  def check_col(self, token, colour, update=False):
    tx = token.get_x()
    ty = token.get_y()
    top, bottom = None, None
    y = ty - 1
    while y >= 0: # scan to the top of the token to find a top flank
      currtok = self.board.get_token(tx, y)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        top = y # set the y-coord of the topmost flank
      else:
        if update:
          self.board.update(tx, y)
      y -= 1
    y = ty + 1
    while y < self.board.get_size(): # scan to the bottom of the token to find a right flank
      currtok = self.board.get_token(tx, y)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        bottom = y # set the y-coord of the bottom-most flank
      else:
        if update:
          self.board.update(tx, y)
      y += 1
    if top is None and bottom is None:
      return False
    return True
  def check_diag(self, token, colour, update=False):
    tx = token.get_x()
    ty = token.get_y()
    x, y = tx-1, ty-1
    topleft, topright, botleft, botright = None, None, None, None
    while x >= 0 and y >= 0:
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour:
        topleft = (x, y)
      else:
        if update:
          self.board.update(x, y)
      x -= 1
      y -= 1
    x, y = tx+1, ty+1
    while x < self.board.get_size() and y < self.board.get_size():
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour:
        botright = (x, y)
      else:
        if update:
          self.board.update(x, y)
      x += 1
      y += 1
    x, y = tx-1, ty+1
    while x < self.board.get_size() and y >= 0:
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour:
        botleft = (x, y)
      else:
        if update:
          self.board.update(x, y)
      x -= 1
      y += 1
    x, y = tx+1, ty-1
    while x >= 0 and y < self.board.get_size():
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour:
        topright = (x, y)
      else:
        if update:
          self.board.update(x, y)
      x += 1
      y -= 1
    if any([topleft, topright, botleft, botright]):
      return True
    return False
  def premove(self):
    # check if the game has finished:
    # if there are no more possible moves by either player (generally, no more empty squares)
    valids = self.valid_moves(self.get_currplayercolr())
    other_valids = self.valid_moves('W' if self.get_currplayercolr() == 'B' else 'B')
    if len(valids) == 0 and len(other_valids) == 0:
      print 'The game has ended! ___ wins!\n' # TO BE IMPLEMENTED
      return 1
    if len(valids) == 0: # curr player has no valid moves, so skips a turn
      print '%s has no valid moves this turn, so we move to the other player!\n' % self.get_currplayername()
      self.curr_player = int(not self.curr_player)
    return 0 # not really needed
  def __str__(self):
    gamestr = "This is a %sx%s game of Othello. It's %s's turn to move.\n" \
      % (self.size, self.size, self.get_currplayername())
    return gamestr + str(self.board)
  def run(self):
    while 1:
      ret = self.premove()
      if ret == 1:
        break
      print self
      nx, ny = self.get_move()
      self.make_move(nx, ny)

if __name__ == '__main__':
  g = Game()
  g.run()
