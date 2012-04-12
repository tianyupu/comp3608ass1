class token(object):
  stability = 1 # weighting of stability that the token currently has
  def __init__(self, x, y, colour):
    self.x = x
    self.y = y
    self.colour = colour
  def flip(self):
    self.colour = self.colour=='black' and 'white' or 'black'
  def stabilise(st):
    stability = st

class board(object):
  tokens = []
  def __init__(self, size): #anything else?
    self.size = size
  def display(self):
    # displays board
    for y in xrange(size):
      for x in xrange(size):
        if token(x,y) in tokens:
          if token(x,y) is black:
            print 'b'
          else:
            print 'w'
        else:
          print '*'
      print
  def move(self, token):
    colour = token.colour
    if colour == black:
      other = white
    else:
      other = black
    # places piece on board and changes affected pieces
    tokens.append(token)
    # check all adjacent pieces to find one of opposite colour
    search = neighbours(token, other)
    for square in search:
      if(valid_row()):
        move(token,valid_row())
