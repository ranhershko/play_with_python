def get_full_line(x = 0, y = 0, star1=1, star2=1):
  global ready_line
  if ( (star1 == star2 and x == y) or ((x == star1 or x == star2) and (y == star1 or y == star2))):
    ready_line = ready_line + "*"
  else:
    ready_line = ready_line + " "

not_odd = True
odd = 0
while not_odd:
  odd = input("Enter odd number for x stars size: ")
  if not odd.isdigit() or int(odd) % 2 == 0:
    print(f"{odd} isn't a number or isn't an odd number")
  else:
    odd = int(odd)
    not_odd = False

star_size = odd + 1
for row in range(1,star_size):
  ready_line = ""
  for col in range(1,star_size):
    if col == star_size / 2 and row == star_size:
      get_full_line(col, row, col, row)
    else:
      get_full_line(col, row, col, star_size - col)
    if col == star_size - 1:
      print(ready_line)