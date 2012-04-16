#!/usr/bin/python

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
  def change_colour(self, colour=None):
    """Changes the colour of the token. If colour is provided, change the colour
    of the token to the one indicated. If colour is omitted, flips the colour
    of the token to the other colour."""
    if not colour:
      if self.colour == 'B':
        self.colour = 'W'
      else:
        self.colour = 'B'
    elif colour in 'BW':
      self.colour = colour
  def stabilise(self, st): # not used currently
    """Changes the stability of the token to st."""
    self.stability = st
  def __str__(self):
    return self.colour
  def __repr__(self):
    return '(%s, %s)' % (self.x, self.y)
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
    """Returns a player-friendly representation of the board that is printable."""
    horizcoords = ' ' + ''.join([str(i) for i in xrange(self.size)]) + ' '
    topborder = '+%s+' % ('-' * self.size)
    boardgrid = [horizcoords, topborder]
    for i in xrange(self.size):
      row = '|' + ''.join([t.get_colour() for t in self.tokens[i]]) + '|%s' % i
      boardgrid.append(row)
    boardgrid.append(topborder)
    boardstr = '\n'.join(boardgrid)
    return boardstr
  def update_token(self, x, y, colour=None):
    """Updates the token at (x, y) by flipping its colour. If colour is given,
    changes the blank token at that position to be the colour indicated."""
    if not colour:
      self.tokens[y][x].change_colour()
    elif colour in 'BW':
      self.tokens[y][x].change_colour(colour)
  def get_size(self):
    return self.size
  def get_token(self, x, y):
    """Get the token in the board at a particular coordinate indicated by (x, y).
    If the index is out of bounds, return None."""
    if x < 0 or x > self.get_size()-1 or y < 0 or y > self.get_size()-1:
      return None
    return self.tokens[y][x]
  def get_adjacent(self, x, y):
    """Returns a list of the 8 tokens surrounding the token located at (x, y).
    If no tokens exist because the coordinates are off the board, then one or
    more Nones will appear in the resulting list."""
    toks = [self.get_token(x,y-1), self.get_token(x,y+1), self.get_token(x-1,y), self.get_token(x+1,y)]
    return toks
  def get_alltoks(self):
    """Return a list of all tokens on the board as a one-dimensional list."""
    toks = []
    for i in xrange(self.size):
      for j in xrange(self.size):
        toks.append(self.tokens[j][i])
    return toks
# def get_row(self, y):
#   """Returns a row of the board as a list, given the y-coordinate, or None if the
#   row does not exist.
#   """
#   if y < 0 or y > self.get_size()-1:
#     return None
#   return self.tokens[y]
# def get_column(self, x):
#   if x < 0 or y > self.get_size()-1:
#     return None
#   toks = []
#   for i in xrange(self.get_size()):
#     toks.append(self.tokens[i][x])
#   return toks
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
    line = raw_input("Type your move in the form 'x y' (without quotes): ").strip()
    x, y = line.split()
    return int(x), int(y)
  def make_move(self, x, y, moveset):
    newcolour = self.get_currplayercolr()
    self.board.update_token(x, y, newcolour)
    self.curr_player = int(not self.curr_player) # switch player turn
    row, col, diag = moveset[(x, y)]
    if row:
      left, right = row
      if left:
        for i in xrange(left+1, x):
          self.board.update_token(i, y, newcolour)
      if right:
        for i in xrange(x+1, right):
          self.board.update_token(i, y, newcolour)
    if col:
      top, bottom = col
      if top:
        for i in xrange(top+1, y):
          self.board.update_token(x, i, newcolour)
      if bottom:
        for i in xrange(y+1, bottom):
          self.board.update_token(x, i, newcolour)
    if diag:
      topl, topr, botl, botr = diag
      if topl:
        nx, ny = topl
        nx += 1
        ny += 1
        while nx < x and ny < y:
          self.board.update_token(nx, ny, newcolour)
          nx += 1
          ny += 1
      if botr:
        nx, ny = botr
        nx -= 1
        ny -= 1
        while nx > x and ny > y:
          self.board.update_token(nx, ny, newcolour)
          nx -= 1
          ny -= 1
      if topr:
        nx, ny = topr
        nx -= 1
        ny += 1
        while nx > x and ny < y:
          self.board.update_token(nx, ny, newcolour)
          nx -= 1
          ny += 1
      if botl:
        nx, ny = botl
        nx += 1
        ny -= 1
        while nx < x and ny > y:
          self.board.update_token(nx, ny, newcolour)
          nx += 1
          ny -= 1
  def valid_moves(self, colour):
    moves = {}
    candidates = set()
    other_col = 'W' if colour == 'B' else 'B'
    for tok in self.board.get_alltoks():
      # here we are checking
      # 1. find a token of the oponnents colour
      # 2. check that it has a blank square next to it
      # 3. check that on the opposite side of the blank square is either:
      # a token of your colour or a row/column of the opponents colour then your own
      if tok.get_colour() == other_col: # if the colour of the token is of the opposing side,
        adj = self.board.get_adjacent(tok.get_x(), tok.get_y()) # get all its adjacent tokens
        for adjtoken in adj:
          if adjtoken is not None and adjtoken.get_colour() == ' ': # if any of these adjacent tokens are blank,
            candidates.add(adjtoken) # then it's a possible place to put our next token
    for c in candidates:
      ret = self.has_move(c, colour)
      if ret:
        cx, cy = c.get_x(), c.get_y()
        moves[(cx,cy)] = ret
    return moves
  def has_move(self, token, colour):
    row = self.check_row(token, colour)
    col = self.check_col(token, colour)
    diag = self.check_diag(token, colour)
    if any([row, col, diag]):
      return row, col, diag
    return False
  def check_row(self, token, colour):
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
      x -= 1
    x = tx + 1
    while x < self.board.get_size(): # scan to the right of the token to find a right flank
      currtok = self.board.get_token(x, ty)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        right = x # set the x-coord of the leftmost flank
      x += 1
    if (left is None or tx-left == 1) and (right is None or right-tx == 1):
      return False
    return left, right
  def check_col(self, token, colour):
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
      y -= 1
    y = ty + 1
    while y < self.board.get_size(): # scan to the bottom of the token to find a right flank
      currtok = self.board.get_token(tx, y)
      if currtok.get_colour() == ' ':
        break # if there's a blank space there, there's nothing to flank
      if currtok.get_colour() == colour:
        bottom = y # set the y-coord of the bottom-most flank
      y += 1
    if (top is None or ty-top == 1) and (bottom is None or bottom-ty == 1):
      return False
    return top, bottom
  def check_diag(self, token, colour):
    tx = token.get_x()
    ty = token.get_y()
    x, y = tx-1, ty-1
    coords = [None, None, None, None] # topl, topr, botl, botr
    while x >= 0 and y >= 0:
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour and tx-x > 1 and ty-y > 1:
        coords[0] = (x, y)
      x -= 1
      y -= 1
    x, y = tx+1, ty+1
    while x < self.board.get_size() and y < self.board.get_size():
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour and x-tx > 1 and y-ty > 1:
        coords[3] = (x, y)
      x += 1
      y += 1
    x, y = tx-1, ty+1
    while x >= 0 and y < self.board.get_size():
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour and tx-x > 1 and y-ty > 1:
        coords[2] = (x, y)
      x -= 1
      y += 1
    x, y = tx+1, ty-1
    while x < self.board.get_size() and y >= 0:
      currtok = self.board.get_token(x, y)
      if currtok.get_colour() == ' ':
        break
      if currtok.get_colour() == colour and x-tx > 1 and ty-y > 1:
        coords[1] = (x, y)
      x += 1
      y -= 1
    if any(coords):
      return tuple(coords)
    return False
  def premove(self):
    # check if the game has finished:
    # if there are no more possible moves by either player (generally, no more empty squares)
    valids = self.valid_moves(self.get_currplayercolr())
    other_valids = self.valid_moves('W' if self.get_currplayercolr() == 'B' else 'B')
    if len(valids) == 0 and len(other_valids) == 0:
      print 'The game has ended! ___ wins!' # TO BE IMPLEMENTED: says who wins and the score
      return 1
    if len(valids) == 0: # curr player has no valid moves, so skips a turn
      print '%s has no valid moves this turn, so we move to the other player!' % self.get_currplayername()
      self.curr_player = int(not self.curr_player)
      return 2
    return valids
  def __str__(self):
    gamestr = "This is a %sx%s game of Othello. It's %s's turn to move.\n" \
      % (self.size, self.size, self.get_currplayername())
    return gamestr + str(self.board)
  def run(self):
    while 1:
      ret = self.premove()
      if ret == 1:
        break
      if ret == 2:
        continue
      print self
      print ret
      nx, ny = self.get_move()
      while (nx, ny) not in ret:
        print "The move you entered was invalid. Please try again!"
        nx, ny = self.get_move()
      self.make_move(nx, ny, ret)

if __name__ == '__main__':
  g = Game()
  g.run()
