# alpha-beta search
won = 10000
lost = -10000

# start by doing basic minimax
# but add in additional checks to allow break points i.e. pruning
# def alpha_beta(game, alpha, beta, depth = 4):

  # def max_val(game, level, alpha, beta):
    # level = level + 1
    # if level <= depth:
      # value = lost
      # for move in valid_moves():
        # value = max(value,min_val(eval1(move), alpha, beta))
        # if value >= beta:
          # return value
        # alpha = max(alpha, value)
      # return value
    # else:
      # return lost #smallest possible heuristic therefore will never be chosen

  # def min_val(game, level, alpha, beta):
    # level = level + 1
    # if level <= depth:
      # value = won
      # for move in valid_moves():
        # value = min(value, max_value(eval1(move), alpha, beta))
        # if value <= alpha:
          # return value
        # beta = min(beta, value)
      # return value
    # else:
      # return won #largest possible heuristic therefore will never be chosen

  # def eval1(game, x, y, which):
    # moveset = game.valid_moves(which)[0]
    # new = copy.copy(game)
    # new = game.make_move(move[0],move[1], moveset)
    # print type(game), type(new)
    # print new.board
    # if which=="white":
      # return new.board.get_white()
    # else:
      # return new.board.get_black()

  # def eval2(move, colour):
    # moveset = game.valid_moves(which)[0]
    # new = game.make_move(move[0],move[1], moveset)
    # heur = 0
    #for each token multiply it by stability and add them up
    # toks = new.board.get_alltoks()
    # for tok in toks:
      # if tok.get_colour() == colour:
        # heur += tok.stability()
    #add twice the number of possible moves
    # heur += 2*len(new.valid_moves)

  # level = 1
  # moves = game.valid_moves('W')[1]
  # best = [moves[0],0]
  # for move in moves:
    # val = min_val(game, 'B', level)
    # level = 1
    # if val[1] > best[1]:
      # best = val
  # return best[0]

  # return a

def alphabeta(node, depth, alpha, beta, player_col):
  other_col = 'W' if player_col == 'B' else 'B'
  if depth == 0 or len(node.get_children()) == 0:
    return node.eval_1('W')
  if player_col == 'W': # W is the maxplayer
    for child in node.get_children():
      alpha = max(alpha, alphabeta(child, depth-1, alpha, beta, other_col))
      if beta <= alpha:
        break
    return alpha
  else:
    for child in node.get_children():
      beta = min(beta, alphabeta(child, depth-1, alpha, beta, other_col))
      if beta <= alpha:
        break
    return beta