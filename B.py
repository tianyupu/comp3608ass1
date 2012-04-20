# alpha-beta search
won = 10000
lost = -10000

# start by doing basic minimax
# but add in additional checks to allow break points i.e. pruning

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
