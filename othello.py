#!/usr/bin/python

import othello
import A
import B
import C
import tree

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
    of the token to the other colour.

    Returns a 2-tuple (colour, flag) where colour indicates the colour of the
    new token and flag=0 indicates adding a new coloured token, flag=1 indicates
    updating the colour of an existing token."""
    if self.get_colour() == ' ':
      flag = 0
    elif self.get_colour() in 'BW':
      flag = 1
    if not colour: # if no colour provided, just flip the colour
      if self.colour == 'B':
        self.colour = 'W'
      elif self.colour == 'W':
        self.colour = 'B'
    elif colour in 'BW':
      self.colour = colour
    return (self.colour, flag)
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
  def get_stability(self):
    return self.stability
  def __ne__(self, other):
    if other.get_x() != self.x or other.get_y() != self.y or other.get_colour != self.colour:
      return True
    return False

class Board(object):
  def __init__(self, size):
    self.size = size
    self.tokens = []
    self.tokencount = {'W': 2, 'B': 2}
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
    horizcoords = ' ' + ' '.join([str(i) for i in xrange(self.size)]) + ' '
    topborder = '+%s+' % ('-' * self.size * 2)
    boardgrid = [horizcoords, topborder]
    for i in xrange(self.size):
      row = '|' + ' '.join([t.get_colour() for t in self.tokens[i]]) + '|%s' % i
      boardgrid.append(row)
    boardgrid.append(topborder)
    boardstr = '\n'.join(boardgrid)
    return boardstr
  def update_token(self, x, y, colour=None):
    """Updates the token at (x, y) by flipping its colour. If colour is given,
    changes the blank token at that position to be the colour indicated."""
    newcolour, ret = self.tokens[y][x].change_colour(colour)
    if ret == 0: # adding a token (ie. updating a blank with a colour)
      self.tokencount[newcolour] += 1
    elif ret == 1:
      self.tokencount[newcolour] += 1
      oldcolour = 'W' if newcolour == 'B' else 'B'
      self.tokencount[oldcolour] -= 1
  def get_size(self):
    return self.size
  def get_token(self, x, y):
    """Get the token in the board at a particular coordinate indicated by (x, y).
    If the index is out of bounds, return None."""
    if x < 0 or x > self.get_size()-1 or y < 0 or y > self.get_size()-1:
      return None
    return self.tokens[y][x]
  def get_adjacent(self, x, y):
    """Returns a list of the 4 tokens surrounding the token located at (x, y).
    If no tokens exist because the coordinates are off the board, then one or
    more Nones will appear in the resulting list."""
    toks = [self.get_token(x,y-1), self.get_token(x,y+1), self.get_token(x-1,y), self.get_token(x+1,y)]
    return toks
  def get_neighbours(self, x, y):
    """Returns a list of the 8 tokens surrounding the token located at (x, y),
    including diagonals.
    If no tokens exist because the coordinates are off the board, then one or
    more Nones will appear in the resulting list."""
    toks = []
    for i in [x-1,x,x+1]:
      for j in [y-1,y,y+1]:
        if i == x and j == y:
          continue
        toks.append(self.get_token(i,j))
    return toks
  def get_alltoks(self):
    """Return a list of all tokens on the board as a one-dimensional list."""
    toks = []
    for i in xrange(self.size):
      for j in xrange(self.size):
        toks.append(self.tokens[j][i])
    return toks
  def get_white(self):
    """Returns the number of white tokens on the board."""
    return self.tokencount['W']
  def get_black(self):
    """Returns the number of black tokens on the board."""
    return self.tokencount['B']

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
  def __init__(self, size=8, level=0):
    """Creates a new Othello game.

    Arguments:
    size -- the desired size of the Othello board (default 8)
    level -- the desired difficulty of the computer opponent (default 0).
    This affects the depth of the search space in the mini-max algorithm etc.
    """
    abc = {'A':'Amy','B':'Ben','C':'Cameron'}
    self.size = size
    self.level = level
    self.board = Board(size)
    self.comp = raw_input("Which AI would you like to play against? Amy (A), Ben (B), Cameron (C), or human (H): \n")
    if self.comp == 'H':
      self.players = [Player(raw_input("Black player please type your name\n"),'B'), Player(raw_input("White player please type your name\n"), 'W')]
    else:
      self.level = int(raw_input("Which level would you like to play at: 1, 2 or 3?\n")) + 2 # makes base level depth of three
      self.players = [Player(raw_input("You are black, please type your name\n"),'B'), Player(abc[self.comp], 'W')]
    self.curr_player = 0
    self.moves_made = []
  def copy(self):
    import copy
    return copy.deepcopy(self)
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
  def comp_move(self):
    if self.comp == 'A':
      move = A.minimax(self, self.level)
#      self.make_move(move[0],move[1],self.premove())
    elif self.comp == 'B':
      move = alphabeta(self.board, self, alpha, beta, level)
#      self.make_move(move)
    else:
      move = master(self.board, self,level)
    return move
  def make_move(self, x, y, moveset):
    self.moves_made.append((x,y))
    newcolour = self.get_currplayercolr()
    self.board.update_token(x, y, newcolour) # place a token at this new spot (x,y)
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
        adj = self.board.get_neighbours(tok.get_x(), tok.get_y()) # get all its neighbour tokens
        for adjtoken in adj:
          if adjtoken is not None and adjtoken.get_colour() == ' ': # if any of these neighbour tokens are blank,
            candidates.add(adjtoken) # then it's a possible place to put our next token
    for c in candidates:
      ret = self.has_move(c, colour, other_col)
      if ret:
        cx, cy = c.get_x(), c.get_y()
        moves[(cx,cy)] = ret
    return moves, moves.keys()
  def has_move(self, token, colour, other_col):
    row = self.check_row(token, colour, other_col)
    col = self.check_col(token, colour, other_col)
    diag = self.check_diag(token, colour, other_col)
    if any([row, col, diag]):
      return row, col, diag
    return False
  def check_row(self, token, colour, other_col):
    tx = token.get_x()
    ty = token.get_y()
    left, right = None, None
    othertoks = 0
    x = tx - 1
    while x >= 0: # scan to the left of the token to find a left flank
      currcolour = self.board.get_token(x, ty).get_colour()
      if currcolour == ' ':
        break # if there's a blank space there, there's nothing to flank
      elif currcolour == colour and othertoks > 0:
        left = x # set the x-coord of the first token of our colour if we've seen other coloured tokens
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x -= 1
    x = tx + 1
    othertoks = 0
    while x < self.board.get_size(): # scan to the right of the token to find a right flank
      currcolour = self.board.get_token(x, ty).get_colour()
      if currcolour == ' ':
        break # if there's a blank space there, there's nothing to flank
      elif currcolour == colour and othertoks > 0:
        right = x # set the x-coord of the first token of our colour if we've seen other coloured tokens
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x += 1
    if left is None and right is None:
      return False
    return left, right
  def check_col(self, token, colour, other_col):
    tx = token.get_x()
    ty = token.get_y()
    top, bottom = None, None
    othertoks = 0
    y = ty - 1
    while y >= 0: # scan to the top of the token to find a top flank
      currcolour = self.board.get_token(tx, y).get_colour()
      if currcolour == ' ':
        break # if there's a blank space there, there's nothing to flank
      elif currcolour == colour and othertoks > 0:
        top = y # set the y-coord of the first seen top flank
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      y -= 1
    y = ty + 1
    othertoks = 0
    while y < self.board.get_size(): # scan to the bottom of the token to find a right flank
      currcolour = self.board.get_token(tx, y).get_colour()
      if currcolour == ' ':
        break # if there's a blank space there, there's nothing to flank
      elif currcolour == colour and othertoks > 0:
        bottom = y # set the y-coord of the first seen bottom flank
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      y += 1
    #if (top is None or ty-top == 1) and (bottom is None or bottom-ty == 1):
    if top is None and bottom is None:
      return False
    return top, bottom
  def check_diag(self, token, colour, other_col):
    tx = token.get_x()
    ty = token.get_y()
    othertoks = 0
    x, y = tx-1, ty-1
    coords = [None, None, None, None] # topl, topr, botl, botr
    while x >= 0 and y >= 0:
      currcolour = self.board.get_token(x, y).get_colour()
      if currcolour == ' ':
        break
      #if currtok.get_colour() == colour and tx-x > 1 and ty-y > 1:
      elif currcolour == colour and othertoks > 0:
        coords[0] = (x, y)
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x -= 1
      y -= 1
    x, y = tx+1, ty+1
    othertoks = 0
    while x < self.board.get_size() and y < self.board.get_size():
      currcolour = self.board.get_token(x, y).get_colour()
      if currcolour == ' ':
        break
      #if currtok.get_colour() == colour and x-tx > 1 and y-ty > 1:
      elif currcolour == colour and othertoks > 0:
        coords[3] = (x, y)
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x += 1
      y += 1
    x, y = tx-1, ty+1
    othertoks = 0
    while x >= 0 and y < self.board.get_size():
      currcolour = self.board.get_token(x, y).get_colour()
      if currcolour == ' ':
        break
      #if currtok.get_colour() == colour and tx-x > 1 and y-ty > 1:
      elif currcolour == colour and othertoks > 0:
        coords[2] = (x, y)
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x -= 1
      y += 1
    x, y = tx+1, ty-1
    othertoks = 0
    while x < self.board.get_size() and y >= 0:
      currcolour = self.board.get_token(x, y).get_colour()
      if currcolour == ' ':
        break
      #if currtok.get_colour() == colour and x-tx > 1 and ty-y > 1:
      elif currcolour == colour and othertoks > 0:
        coords[1] = (x, y)
        break
      elif currcolour == colour:
        break
      elif currcolour == other_col:
        othertoks += 1
      x += 1
      y -= 1
    if any(coords):
      return tuple(coords)
    return False
  def premove(self):
    # check if the game has finished:
    # if there are no more possible moves by either player (generally, no more empty squares)
    valids = self.valid_moves(self.get_currplayercolr())[0]
    other_valids = self.valid_moves('W' if self.get_currplayercolr() == 'B' else 'B')[0]
    if len(valids) == 0 and len(other_valids) == 0:
      # print out final game position
      print self
      # finding out who the winner is
      nwhite = self.board.get_white()
      nblack = self.board.get_black()
      winner = ''
      print 'White: %d, Black: %d' % (nwhite, nblack)
      if nwhite > nblack:
        print 'White wins!'
        winner = 'W'
      elif nblack > nwhite:
        print 'Black wins!'
        winner = 'B'
      else:
        print "The game has ended! It's a tie =)"
        return 1
      return 1
    if len(valids) == 0: # curr player has no valid moves, so skips a turn
      print '%s has no valid moves this turn, so we move to the other player!' % self.get_currplayername()
      self.curr_player = int(not self.curr_player) # flip the player
      return 2
    return valids
  def __str__(self):
    gamestr = "This is a %sx%s game of Othello. It's %s's (%s) turn to move.\n" \
      % (self.size, self.size, self.get_currplayername(), self.get_currplayercolr())
    return gamestr + str(self.board)
  def run(self):
    while 1:
      ret = self.premove()
      if ret == 1:
        break
      if ret == 2:
        continue
      print self
      print '==> MOVES MADE SO FAR:', self.moves_made
      print 'White: %d, Black: %d' % (self.board.get_white(), self.board.get_black())
      print 'Your valid moves are:', self.valid_moves(self.get_currplayercolr())[1]
      if self.get_currplayercolr() == 'B' or self.comp == 'H':
        nx, ny = self.get_move()
        while (nx, ny) not in ret:
          print "The move you entered was invalid. Please try again!"
          nx, ny = self.get_move()
      elif self.comp == 'A':
        nx, ny = self.comp_move()
      self.make_move(nx, ny, ret)

if __name__ == '__main__':
  g = Game()
  g.run()
