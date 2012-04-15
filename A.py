# Minimax Algorithm
import util

possible = valid_moves()
optimal = []
#should put these for loops into a loop going until "depth"
level = 1
#okay so i need a loop of loops:
# the outer loop should go through the depths
# the inner loop should calculate an evaluation and choose the min and the max
# in alternating turns
while level < depth:
  for move in possible:
    this = make_move()
    choices = valid_moves()
    temp = []
    for choice in choices:
      value = evaluate(choice)
      temp.add(choice,value)
    optimal.add(max(temp))
  level = level + 1
move = max(optimal)
make_move(move)
