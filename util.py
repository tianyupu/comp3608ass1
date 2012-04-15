# Constants
depth = 3 # how many moves ahead to look
won = 10000
lost = -10000
size = 8 # size of board
const = 3 # number for heuristic that you multiply the importance of quantity of coins by

# Functions
def move(token1, token2):
  # flip all pieces in row to colour corresponding to end 2 tokens
  # step one determine whether diag, row or column
  # step 2 iterate through appropriate one calling flip on each token
  x = token1.x
  y = token1.y
  x1 = token2.x
  y2 = token2.y
  if x == x1:
    if y < y1:
      for i in xrange(y,y1):
        token(x,i).flip()
    else:
      for i in xrange(y1,y):
        token(x,i).flip()
  elif y == y1:
    if x < x1:
      for j in xrange(x,x1):
        token(j,y).flip()
    else:
      for j in xrange(x1,x):
        token(j,y).flip()
  else:
    if x < x1 and y < y1:
      for i in xrange(x,x1):
        for j in xrange(y,y1):
          token(i,j).flip()
    elif x > x1 and y < y1:
      for i in xrange(x1,x):
        for j in xrange(y,y1):
          token(i,j).flip()
    elif x < x1 and y > y1:
      for i in xrange(x,x1):
        for j in xrange(y1,y):
          token(i,j).flip()
    else:
      for i in xrange(x1,x):
        for j in xrange(y1,y):
          token(i,j).flip()
  return 0
  # SURELY THERE IS A NEATER WAY TO DO THIS... TO DO LATER

def valid_moves(board, colour):
  if colour == black:
    other = white
  else:
    other = black
  # returns a list of valid moves
  moves = []
  # for each other_colour piece on the board:
  #   if it has an adjacent blank piece next to it remember and check if it has one of your own next to it...
  #   or in the row/column/diagnonal next to it
  pieces = []
  for token in board.tokens:
    if token.colour == other:
      pieces.append(token)
  search = []
  for token in pieces:
    mysearch = neighbours(token,blank)
    search.append(mysearch)

  # check if each move is valid and evaluate new heuristic
  for tokens in search:
    for possible in tokens:
      if valid_row(possible, piece[tokens], board):
        value = evaluate(row)
        moves.append(token, value) # token is the piece you are placing
  return moves

def valid_row(newToken, oldToken, board):
  valid = False
  found = False
  token = NULL
  # it continues along row/column/diagonal to see if the end of that row/column diagonal has your piece in it,
  # returns true(eventually hits new colour piece) or false (eventually hits a blank)
  x = newtoken.x
  y = newtoken.y
  x1 = oldtoken.x
  y2 = oldtoken.y
  if x == x1:
    i = y
    if y < y1:
      while i < size and not found:
        if not token(x,i) or token(x,i).colour == newToken.colour:
          found = true
          if token(x,i).colour == newToken.colour:
            valid = true
            token = token(x,i)
        i = i + 1
    else:
      while i < 0 and not found:
        if not token(x,i) or token(x,i).colour == newToken.colour:
          found = true
          if token(x,i).colour == newToken.colour:
            valid = true
            token = token(x,i)
        i = i - 1
  elif y == y1:
    j = x
    if x < x1:
      while j < size and not found:
        if not token(x,j) or token(x,j).colour == newToken.colour:
          found = true
          if token(x,j).colour == newToken.colour:
            valid = true
            token = token(j,y)
        i = i + 1
    else:
      while j > 0 and not found:
        if not token(x,j) or token(x,j).colour == newToken.colour:
          found = true
          if token(x,j).colour == newToken.colour:
            valid = true
            token = token(j,y)
        i = i - 1
  else:
    if x < x1 and y < y1:
      for i in xrange(x,x1):
        for j in xrange(y,y1):
          while j < size and i < size and not found:
            if not token(i,j) or token(i,j).colour == newToken.colour:
              found = true
              if token(i,j).colour == newToken.colour:
                valid = true
                token = token(i,j)
            i = i + 1
            j = j + 1
    elif x > x1 and y < y1:
      for i in xrange(x1,x):
        for j in xrange(y,y1):
          while j < size and i > 0 and not found:
            if not token(i,j) or token(i,j).colour == newToken.colour:
              found = true
              if token(i,j).colour == newToken.colour:
                valid = true
                token = token(i,j)
            i = i - 1
            j = j + 1
    elif x < x1 and y > y1:
      for i in xrange(x,x1):
        for j in xrange(y1,y):
          while j > 0 and i < size and not found:
            if not token(i,j) or token(i,j).colour == newToken.colour:
              found = true
              if token(i,j).colour == newToken.colour:
                valid = true
                token = token(i,j)
            i = i + 1
            j = j - 1
    else:
      for i in xrange(x1,x):
        for j in xrange(y1,y):
          while j > 0 and i > 0 and not found:
            if not token(i,j) or token(i,j).colour == newToken.colour:
              found = true
              if token(i,j).colour == newToken.colour:
                valid = true
                token = token(i,j)
            i = i - 1
            j = j - 1
  return token
# THERE MUST BE A NICER WAY OF DOING THIS TO

def evaluate(newToken, oldToken):
  # TO DO
  # returns two integers the first saying how much the playing players heuristic goes up, the second how much the others goes down
  current = 0
  opponent = 0
  search = neighbours(newToken)
  # from oponnent remove number of coins * const
  if newToken == (token(0,0) or token(size,size) or token(0,size) or token(size,0)):
    newToken.stabalise(10)
  # if stablise value not 5 then make value one less than highest neighbour value
  # do this for every flipped token
  # add number of extra coins*const + token.stablise of each token to current
  return (current,opponent)

def neighbours(token,goal):
    # takes arguement type: blank/black/white; and a token
    # returns list of all such neighbours
    search = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if token(i,j) and token(i,j).colour == goal]
    return search
