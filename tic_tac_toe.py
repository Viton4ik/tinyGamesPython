# ИТОГОВОЕ ЗАДАНИЕ 5.6 (HW-02) - Skillfactory
# Victor Vetoshkin
# August 2022
#version 2.0
    # * --- checking for a digit range to put in added
    # ** --- checking if not 'integer' was put in added
    # *** --- 'draw' condition added
    # **** --- win condition reduced
# rev.03
    #  **** --- fast 'draw' condition has been added

import time

# Define a field
field = ['[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]','[ ]']

# Print a field
def field_print(i = 6,j = 9):
    while j >= 3:
        if i % 3 == 0 and j % 3 == 0:
            print(*field[i:j], end = '\n')
            i -= 3
            j -= 3

# Win Conditions  ****
def win():
    con_var = [
        (6, 7, 8), #\
        (3, 4, 5), # | horizontal lines
        (0, 1, 2), #/
        (0, 3, 6), #\
        (1, 4, 7), # | vertical lines
        (2, 5, 8), #/
        (2, 4, 6), #\  diagonal lines
        (0, 4, 8)  #/
    ]
    for condition in con_var:
        if field[condition[0]] == '[0]' and field[condition[1]] == '[0]' and field[condition[2]] == '[0]':
            return 1
        if field[condition[0]] == '[X]' and field[condition[1]] == '[X]' and field[condition[2]] == '[X]':
            return 1

# The Game
print("-------- Tic-Tac-Toe game. @Created by Victor Vetoshkin --------\n")
print('Use Numpad digits (1-9 digit) to select a place on the field')
field_print() # Print the field
player = '[X]'  # First player - X
count = 0       # count steps
while not win():
    try:        # ** - checking if not 'integer' was put in
        digit = int(input(f"Put {player} on the field (use 1-9 digit), 0 - abort the game: "))
        if 0 <= digit <= 9: # * - checking for a digit range to put in
            if digit != 0:
                if field[digit-1] == '[ ]':
                    field[digit-1] = player           # rewrite the place on the field with X or O
                    field_print()                     # print new field
                    if not win():                     # Stop counting steps if we have a winner
                        count += 1                    # next step
                        if count % 2 == 0:            # choose the player
                            player = '[X]'
                        else:
                            player = '[0]'
                        if count == 7:  # **** --- fast 'draw' condition has been added
                            key = input("There is no way to win now!\n "
                                  "If you want to proceed press 'y' or press any key to abort")
                            if key == 'y':
                                pass
                            else:
                                print('The game has finished in a draw!')
                                break
                        if count == 9: # *** --- 'draw' condition has been added
                            print('The game has finished in a draw!')
                            break
                else:
                    print("\nThis place has already used on the filed. Please choose another place.\n")
            else:
                print('\nThe Game has been aborted by a player')
                break
        else: # * - checking for a digit range to put in
            print("\nPlease use 1-9 digits ONLY to select place on a field, or 0 - abort the game \n")
    except ValueError: # ** ---checking if not integer was put
        print("\nPlease use 1-9 digits ONLY to select place on a field, or 0 - abort the game \n")

if digit != 0 and win():
    print(f"The '{player}' - player won!")

time.sleep(1) # delay to exit

