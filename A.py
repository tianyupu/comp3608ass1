possible = valid_moves()
optimal = []
#should put these for loops into a loop going until "depth"
for move in possible:
  this = make_move()# make move
  choices = valid_moves()
  temp = []
  for choice in choices:
    value = eval(choice)
    temp.add(choice,value)
  optimal.add(max(temp))
  # THIS WHOLE FUNCTION NEEDS FIXING I'M SLEEPY... JUST SEE IT AS PSEUDOCODE SO FAR =P
move = max(optimal)
make_move(move)

