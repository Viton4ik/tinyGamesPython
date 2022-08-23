# ИТОГОВОЕ ЗАДАНИЕ 5.6 (HW-02) - Skillfactory
# Victor Vetoshkin
# August 2022

# Define a field
field = ['[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]']

# Print a field
def field_print(i = 6,j = 9):
    while j >= 3:
        if i % 3 == 0 and j % 3 == 0:
            print(*field[i:j], end = '\n')
            i -= 3
            j -= 3

# Win Conditions
def win():
    # #horizontal lines
    if field[0] == '[0]' and field[1] == '[0]' and field[2] == '[0]':
        return 1
    if field[0] == '[X]' and field[1] == '[X]' and field[2] == '[X]':
        return 1
    if field[3] == '[0]' and field[4] == '[0]' and field[5] == '[0]':
        return 1
    if field[3] == '[X]' and field[4] == '[X]' and field[5] == '[X]':
        return 1
    if field[6] == '[0]' and field[7] == '[0]' and field[8] == '[0]':
        return 1
    if field[6] == '[X]' and field[7] == '[X]' and field[8] == '[X]':
        return 1
    # vertical lines
    if field[0] == '[0]' and field[3] == '[0]' and field[6] == '[0]':
        return 1
    if field[0] == '[X]' and field[3] == '[X]' and field[6] == '[X]':
        return 1
    if field[1] == '[0]' and field[4] == '[0]' and field[7] == '[0]':#
        return 1
    if field[1] == '[X]' and field[4] == '[X]' and field[7] == '[X]':
        return 1
    if field[2] == '[0]' and field[5] == '[0]' and field[8] == '[0]':#
        return 1
    if field[2] == '[X]' and field[5] == '[X]' and field[8] == '[X]':
        return 1
    # diagonal lines
    if field[0] == '[0]' and field[4] == '[0]' and field[8] == '[0]':#
        return 1
    if field[0] == '[X]' and field[4] == '[X]' and field[8] == '[X]':
        return 1
    if field[6] == '[0]' and field[4] == '[0]' and field[2] == '[0]':#
        return 1
    if field[6] == '[X]' and field[4] == '[X]' and field[2] == '[X]':
        return 1

# The Game
print('Use Numpad digits (1-9 digit) to select place on a field')
field_print() # Print the field
player = '[X]'  # First player - X
count = 0       # count steps
while not win():
    digit = int(input(f"Put {player} on the field (use 1-9 digit), 0 - abort the game: "))
    if digit != 0:
        if field[digit-1] == '[ ]':
            field[digit-1] = player           # rewrite the place on the field with X or O
            field_print()                     # print the new field
            if not win():                     # Stop counting steps if a win
                count += 1                    # next step
                if count % 2 == 0:            # choose the player
                    player = '[X]'
                else:
                    player = '[0]'
        else:
            print("This place has already used on the filed. Please choose another place. ")
    else:
        print('\nThe Game has been aborted by a player')
        break
if digit != 0:
    print(f"The '{player}' - player won!")

