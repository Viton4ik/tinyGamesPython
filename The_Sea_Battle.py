from random import randint

# inner logic

class BoardOutException(Exception): # if ship is out of the board
    pass

class PlaceUsageError(Exception): # if a place on the board has been already used
    pass

class WrongLength(Exception): # if ship length is out of range [1 - 4]
    pass

class Dot:
    "Class to create points"
    def __init__(self, x = 0, y = 0): # Initialization method
        self.x = x
        self.y = y

    def __eq__(self, other): # equal method
        return self.x == other.x and self.y == other.y

    def __repr__(self): # print method
        return f"Dot({self.x}, {self.y})"

class Ship:
    "Class describes ships"
    def __init__(self, ship_bow_dot, length, direction): # Initialization method
        self.length = length
        self.ship_bow_dot = ship_bow_dot
        self.direction = direction
        self.lives = length
        self.flag = 0 # flag to print "LengthError" out

    @staticmethod
    def length_check(length): # if Length range is not [1 - 4]
        return not (4 >= length >= 1)

    @property  # get property
    def dots(self):  # print out all ship points
        ship_coord = [] # list for ship coordinates
        ship_point = 0 # counter depends on a ship length
        dot_x = self.ship_bow_dot.x
        dot_y = self.ship_bow_dot.y

        if self.length_check(self.length) and self.flag != 1:
            self.flag = 1 # print it out only once
            print("LengthError! Length range: [1 - 4]")

        if not self.length_check(self.length):
            self.flag = 0 # cancel a flag
            while ship_point != self.length: # if it's okay
                ship_coord.append(Dot(dot_x, dot_y))
                if self.direction == "v": # if vertical
                    dot_x += 1
                elif self.direction == "h": # if horizontal
                    dot_y += 1
                ship_point += 1 # go to the next point

        return ship_coord

class Board:
    "Class describes board features"
    def __init__(self, hid = False):
        self.board_field = [[" "] * 6 for i in range(6)] # all cell list
        self.ship_list = []  # list of ships
        self.hid = hid # True or False
        self.hit_check = 0 # checking the hit
        self.all_ships_coord = [] # collect coordinates for all ships here
        self.shot_list = [] # shots list
        self.contur_point_list = [] # contur points list
        self.killed = 0
        self.destroyed_ship_list = []  # list of ships

    def __str__(self): # print a field
        row_str = "" # start with a no string
        # print()
        print("    | 1 | 2 | 3 | 4 | 5 | 6 | ")
        print("    ------------------------- ")
        for i, row in enumerate(self.board_field):
            for j in range(6):
                if self.hid and (row[j] == "■"): #or row[j] == "."):
                   row[j] = " "
            row_str += f"  {i+1} | {' | '.join(row)} | \n" # fill the field with lines
        row_str += "    ------------------------- "
        return row_str

    def add_ship(self, ship): # put a ship on the board
        for coord in ship.dots:
            if self.out(coord):
                raise BoardOutException("'Your ship is out of the board!'")
            if not self.neighbor(coord):
                raise BoardOutException("'Wrong place!!!The ship has to be replaced'")
            if coord in self.all_ships_coord:
                raise BoardOutException("'Wrong place!!!The ship has to be replaced'")

        for coord in ship.dots: # depict ship
            if coord not in self.all_ships_coord: # if a dot is not being used
                self.board_field[coord.x][coord.y] = "■"
                self.all_ships_coord.append(coord) # save a dot in a ship list
                if not self.hid:  # show contur only for a Player   ###
                    self.contur(ship)             # depict a contur ###

        self.ship_list.append(ship)

    def busy_place(self, point): # if a dot is being used
        if self.board_field[point.x][point.y] == " ":
            return True

    @staticmethod
    def out(point): # if Dot(x,y) is out of the field returns "True"
        return not (((6 > point.x >= 0) and (6 > point.y >= 0)))

    def neighbor(self, point): # if Dot(x,y) is a neighbor returns "True"
        if point not in self.contur_point_list:
            return True

    def contur(self, ship): # ship's area
        for dot in ship.dots: # for each dot in ship
                for i in range(-1, 2): # create a neighbour dot
                    for j in range(-1, 2):
                        near_dot = Dot(dot.x + i, dot.y + j) # create a neighbour dots
                        if not self.out(near_dot) and self.busy_place(near_dot): # check for exceptions and check
                            if ship.lives != 0:
                                self.board_field[near_dot.x][near_dot.y] = " " # put a contur for adding ships
                                self.contur_point_list.append(near_dot)
                            else:
                                self.board_field[near_dot.x][near_dot.y] = "."  # put a contur for destroyed ships
                                self.contur_point_list.append(near_dot)

    def shot(self,shot_coord):

        if self.out(shot_coord):
            raise BoardOutException("'Your shot is out of the board!'")

        if shot_coord in self.shot_list:
            # print("The place has already been shot down!")
            raise BoardOutException("The place has already been shot down!")

        if shot_coord not in self.shot_list and shot_coord not in self.all_ships_coord:
            self.board_field[shot_coord.x][shot_coord.y] = "o"
            print("Miss!\n")
            self.hit_check = 0 # if missed
            # return self.hit_check ####????

        for ship in self.ship_list:
            if shot_coord in ship.dots:
                self.hit_check = 0
                if ship.lives != 0:
                    ship.lives -= 1
                    self.board_field[shot_coord.x][shot_coord.y] = "X"
                    print("Ship has been hit!\n")
                    self.hit_check = 1 # if hit
                    if ship.lives == 0:
                        print(f"The ship with a length '{ship.length}' has been destroyed!\n")
                        self.contur(ship)
                        self.destroyed_ship_list.append(ship.length)
                        self.killed += 1

        self.shot_list.append(shot_coord)
        return self.hit_check # cheking for miss or hit

# outer logic

class Player:
    "Class describes Players"
    def __init__(self, board, ai_board):
        self.board = board
        self.ai_board = ai_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                aim = self.ask()
                fire = self.ai_board.shot(aim)
                return fire
            except BoardOutException as e:
                print(e)

class AI(Player):
    "Class describes AI"
    def ask(self):
        a = randint(0,5)
        b = randint(0,5)
        point = Dot(a, b)
        print(f"Computer's shot: {point.x + 1} {point.y + 1}")
        return point

class User(Player):
    "Class describes User"
    def ask(self):
        while True:
            try:  # checking if not two items were put in
                x, y = input("Put 'x' and 'y' to make a shot: ").split()
            except ValueError:
                print("\n2 coordinates needed \n")
            else:
                try: # checking if not 'integer' was put in
                    x, y = int(x), int(y)
                    if x == 9 and y == 9: # checking for abort
                        print('\nThe Game has been aborted by a Player')
                        break
                    elif not ((6 >= x >= 0) and (6 >= y >= 0)): # if coordinates are out of a range
                        print("\nPlease use digits [1 - 6] ONLY to select coordinates,"
                              "\nOr ['x' = 9, 'y' = 9] - abort game \n")
                    else:
                        return Dot(x - 1, y - 1) # get a Dot
                except ValueError:
                    print("\nPlease use digits [1 - 6] ONLY to select coordinates,"
                          "\nOr ['x' = 9, 'y' = 9] - abort game \n")

class Game:
    "Class describes Game"
    def __init__(self):
        ai = self.random_board_always()
        user = self.random_board_always()
        ai.hid = True
        self.ai = AI(ai, user)
        self.user = User(user, ai)

    def random_board(self):
        board = Board() # define a Board
        rank = (3, 2, 2, 1, 1, 1, 1) # length ships
        direction = ['v', 'h']  # random direction
        count = 0               # numbers of tries
        ships_on_board = 0
        for item in rank:
            while count != 3000:
                count += 1
                # if count > 3000:
                #     return None
                ship = Ship(Dot(randint(0, 5), randint(0, 5)), item, direction[randint(0, 1)])
                try:
                    board.add_ship(ship)
                    ships_on_board += 1 # numbers of ships have been placed on a board
                    break
                except BoardOutException:
                    pass
        if ships_on_board < len(rank): # if ships on a board < 7
            board = "Fault"
            return board
        return board

    def random_board_always(self): # if a board is faulty
        board = "Fault"
        while board == "Fault":
            board = self.random_board() # set it again
        return board

    def greet(self):
        print()
        print("--- @Created by Victor Vetoshkin ---") # delete!!!
        print()                                       # delete!!!
        print("   Welcome to the 'Sea Battle' Game ")
        print("To make a shot use "
              "'x', 'y' coordinates: ")
        print("   'x' - string ")
        print("   'y' - column ")
        print("   ['x' = 9, 'y' = 9] - abort game ")

    def first_shot(self):
        first_shot = randint((self.user.move()),(self.ai.move()))
        return first_shot

    def loop(self):
        print("\n ---Let's start the Game!---\n")
        step = 0
        shots = 0
        while True:
            self.print_status()
            shots += 1
            print("The AI Board:")
            print(self.ai.board)
            print("The User Board:")
            print(self.user.board)
            ai_hit = self.user.board.hit_check
            user_hit = self.ai.board.hit_check
            if (ai_hit == 0 and user_hit == 0) or (ai_hit == 1 and user_hit == 1):
                step += 1
                if step % 2 == 0:
                    print(f"shot №'{shots}'")
                    input("AI is gonna shoot. Press 'Space' then 'Enter' to continue")
                    self.ai.move()
                else:
                    print(f"shot №'{shots}'")
                    self.user.move()
            if ai_hit == 1 and user_hit == 0:
                print(f"shot №'{shots}'")
                input("AI is gonna shoot. Press 'Space' then 'Enter' to continue")
                self.ai.move()
            if ai_hit == 0 and user_hit == 1:
                print(f"shot №'{shots}'")
                self.user.move()
            if self.ai.board.killed == 7: # if all ships destroyed
                print(f"\n!!!User WON!!!")
                print(f"\nGAME OVER")
                break
            if self.user.board.killed == 7: # if all ships destroyed
                print(f"\n----- !!AI WON!! -----")
                print(f"\n----- GAME OVER  -----\n")

    def print_status(self): # status list
        user_ships = []
        user_destroyed_ships = []
        ai_ships = []
        ai_destroyed_ships = []
        for ship in self.user.board.ship_list:
            user_ships.append(ship.length)
        for ship in self.ai.board.ship_list:
            ai_ships.append(ship.length)

        for ship in self.user.board.destroyed_ship_list:
            user_destroyed_ships.append(ship)
            user_ships.remove(ship)
        for ship in self.ai.board.destroyed_ship_list:
            ai_destroyed_ships.append(ship)
            ai_ships.remove(ship)
        print(f"Status for the User's ships:")
        print(f"Combat-ready ships: {user_ships}, Destroyed ships: {user_destroyed_ships}")
        print(f"\nStatus for the AI's ships:")
        print(f"Combat-ready ships: {ai_ships}, Destroyed ships: {ai_destroyed_ships}\n")

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()

