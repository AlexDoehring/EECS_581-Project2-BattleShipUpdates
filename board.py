""" 
    Program name: board.py
    Description: main file that allows two players to play battleship
    Inputs:
    Coordinate for shooting: Users input a grid coordinate (e.g., "A3") to take a shot.
    Movement for placing ships: Users input movement commands to position their ships:
        -W (up), A (left), S (down), D (right) for navigation.
        -R to rotate the ship.
        -C to confirm the ship placement.
        -Q to quit.
    Number of ships: Users input the number of ships to play with (between 1 and 5).
    Confirmation: Players press Enter to confirm or continue certain actions (e.g., turn change or ship confirmation).
    Function Input Parameters:
        -shot: str: The shot taken by a player (e.g., "A3").
        -enemy: Player: The opponent's Player object to check for hit or miss.
        -line_pos_x, line_pos_y, size, horizontal: Coordinates and orientation for placing a ship.
        -grid: The current state of the board/grid for display and manipulation.
        -p1_selection: Boolean value indicating if Player 1 has completed their ship selection.
    Outputs:
    Printed Messages (Console Outputs):
        -"Choose your coordinate to shoot!" or similar messages during gameplay.
        -Messages like "HIT!", "MISS!", and "SHIP DESTROYED!" for shot results.
        -Victory messages such as "Player 0 Wins!" or "Player 1 Wins!" when a player wins.
        -Movement prompts like "Move (W=up, A=left, S=down, D=right, R=rotate, C=confirm, Q=quit):".
        -Grid display during ship placement and gameplay using display_grid().
        -"Overlap detected! Move the line to a new position." if ships overlap.
        -Final boards for both players at the end of the game.
    Return Values:
        -checkHit(): No return, but it prints the result of a shot (hit, miss, ship destroyed).
        -shootShip(): Returns a string representing the shot's coordinate.
        -checkWin(): Returns True if the game should continue and False if the game is won.
        -move_line(): Returns an updated grid with the line placed and the confirmed coordinates.
        -shipPlacement(): Returns two lists of coordinates representing each player's confirmed ship placements.
        -translateCoordinates(): Converts and returns integer tuple coordinates into string grid coordinates (e.g., A3).
        -goodInput(): Returns the number of ships chosen by the user.
    Sources of code: Chat GPT
    Authors: Connor Bennudriti, Brinley Hull, Gianni Louisa, Kyle Moore, Ben Renner
    Creation Date: 8/29/2024
"""
from os import system, name #sets the system name to name
from Ship import Ship #imports the Ship class
from Player import Player #imports the Player class
from Ai import Ai #imports the Ai classs
import random

str_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def checkHit(shot: str, enemy: Player) -> None:
    """
        checkHit(shot: str, enemy: PLayer)

        Sources: Team authored

        Checks whether a shot is a hit or miss and prints the correct message. 
        
        Returns nothing

        Parameters
            shot: a string representing the coordinate of the shot
            enemy: enemy Player object
    """
    hit = False  # Initialize hit as False to prevent issues with the loop

    for enemy_ship in enemy.ships: # Loop through all of the other player's ships
        if shot in enemy_ship.locations:  # Check if the shot hit one of the coordinates held in ship locations
            enemy.last_enemy_shot = shot # (TEAM2 - JAKE) if the shot was a hit, update the enemy's state to record it -- needed for moving ships
            enemy_ship.hit_segments.append(shot)  # Add the section of the ship that was hit to the Ship object's list of hit segments
            print("\nHIT!\n")  # Print HIT to the console
            hit = True  # Set hit to True

            # Check if all segments of the enemy ship have been hit
            if sorted(enemy_ship.hit_segments) == sorted(enemy_ship.locations):
                enemy_ship.destroyed = True  # Set the destroyed ship's bool to true to signify that it was sunk
                print("SHIP DESTROYED!\n")  # Print that the ship was destroyed
            break  # Break the loop after a hit

    if not hit:  # If no hit was detected, print MISS
        enemy.last_enemy_shot = None # (TEAM2 - JAKE) if the shot was not a hit, update the enemy's state to show this
        print("\nMISS!\n")

    # (TEAM2 - JAKE) previously, this was not returned.
    # required for checking if the last shot made by a player was a hit (necessary for AI)
    return hit 


def shootShip(opponent, ai=None) -> str: #If ai parameter is passed, calls ai shootship instead of going to the console
    """
        shootShip(ship_locations: list)

        Sources: Team authored

        Allows a player to input their desired shot coordinates and returns a string representing the coordinates.
        If ai_shot is provided, it uses that as the shot coordinate instead of prompting for input.

        Parameters
            ai_shot: Optional string. The coordinate for AI to shoot. If None, prompts for human input.
    """

    if ai:  # If ai_shot is provided, use it
        shot = ai.shootShip(opponent)
    else:  # Otherwise, prompt the human player
        print("Choose your coordinate to shoot!")  # Print a guiding statement to the user
        while True: # Loop to validate the input coordinate
            shot = input("Coordinate: ").upper() # Player inputs coordinate
            if 2 <= len(shot) <= 3 and shot[0] in columns and shot[1] in str_rows: # If the coordinate is 2 or 3 characters long and the first character is a valid column and the second character is a valid row
                if len(shot) == 3 and (shot[1] + shot[2] not in str_rows): # If the coordinate is three characters long and the two characters at the end aren't in the list of valid rows
                    continue # Stay in the loop
                break # Break out of the loop

    return shot # Return the coordinate of the shot as a string

    
#Gianni Louisa Authored, chatgpt assisted
def checkWin(player): #Alex: Added player parameter to print correct player's win
    """
        checkWin()    
    
        Checks all the players ships to see if they have been destoryed. If all ships are destroyed, the game ends and the winner is printed to the console.
        
        Returns True if the game should continue, 
        Returns False if game is won and should end.
    """

    # Check if all ships of player_zero are destroyed
    if all(ship.destroyed for ship in player.ships):#for every ship in player_zero's ships, check if they are true for destroyed
        print("======================================")#print-out
        print("🎉🎉🎉  CONGRATULATIONS!  🎉🎉🎉")#print-out
        print("======================================")#print-out
        print("      🚢💥 Player 1 Wins! 💥🚢")#print-out
        print("======================================")#print-out
        print("    All enemy ships have been sunk!")#print-out
        print("======================================\n")#print-out
        printFinalBoards() #prints the final boards for each player after the game is over
        return False  # The game ends when player 1 wins
    
    # Check if all ships of player_one are destroyed
    if all(ship.destroyed for ship in player.ships):#for every ship in player_one's ships, check if they are true for destroyed
        print("======================================") #print-out
        print("🎉🎉🎉  CONGRATULATIONS!  🎉🎉🎉")#print-out
        print("======================================")#print-out
        print("      🚢💥 Player 0 Wins! 💥🚢")#print-out
        print("======================================")#print-out
        print("    All enemy ships have been sunk!")#print-out
        print("======================================\n")#print-out
        printFinalBoards() #prints the final boards for each player after the game is over
        return False  # The game ends when player 0 wins
    
    return True  # The game continues if neither player has won yet


def printFinalBoards(player0, player1):
    """Prints the final boards for each player after the game is over."""
    print("player 0's board") #print-out
    player0.printStrikeBoard(player1) #prints player_zero's strike board
    player0.printBoard(player1)  #prints player_zero's board
    print("\nplayer 1's board\n ") #print-out
    player1.printStrikeBoard(player0) #prints player_one's strike board
    player1.printBoard(player0) #prints player_one's board

# (TEAM2 - JAKE)
def grid_coord_to_board_string(x: int, y: int) -> str:
    return columns[x] + str_rows[y] # translate a grid coordinate to a board string by concatenating the values in the arrays used for this
# (TEAM2 - JAKE) End

# (TEAM2 - JAKE)
def make_grid_for_split_placement(grid: list, player: Player, enemy: Player, last_shot: str) -> list:
    """
        make_grid_for_split_placement   
    
        Makes a grid output specifically when a split-off ship needs to be placed.
        Marks all spots hit by the other player and marks all spots taken up by another ship.
        
        Returns an array of strings which represents the board
    """
    for x in range(10): # for all x coordinates
        for y in range(10): # for all y coordinates
            coord = grid_coord_to_board_string(x, y) # translate them to a board string
            if coord == last_shot: # if the board string is the last shot, it should be an "X" for a hit
                grid[y][x] = "X" # shot was a hit 
                continue # continue looping through coords
            if coord in enemy.strike_attempts: # if shot was done by enemy, first set as "O" for miss, later overwritten if it was a hit
                grid[y][x] = "O" # shot was tentatively a miss
            for ship in player.ships: # look through all current player's ships
                if coord in ship.locations and last_shot not in ship.locations: # if the coord was in a ship (that wasn't the one that was hit)
                    if coord in ship.hit_segments: # if the shot was a hit
                        grid[y][x] = "X" # make grid character an X
                    else: # if the ship segment is still alive
                        grid[y][x] = "+" # make the grid character a +
                    break # no need to search through other ships
    return grid # return the filled out grid


# (TEAM2 - JAKE) End


# (TEAM2 - JAKE)
def place_split_ship(player: Player, enemy: Player, last_shot: str, split_ship: Ship, size: int) -> Ship | None:
    """
        place_split_ship

        Sources: Jake, reuse of code from move_line

        Performs the routine for moving ships if a player chooses to "split" a ship that's only been hit once.
        
        Returns the new ship or None.

        Parameters
            player:     the current player
            enemy:      the opponent player
            last_shot:  a string coordinate of the last hit space on the current player's board
            split_ship: the ship that's being split
            size:       the size of the new split ship (should be the old ship's size - 1)
    """
    x_size, y_size = 10, 10 # init grid size
    grid = create_grid(x_size, y_size) # create grid (an arrow of length 10 strings of periods)
    grid = make_grid_for_split_placement(grid, player, enemy, last_shot) # update the grid to show all shots, misses, and placed ships

    clearAndPass() # clear the terminal
    horizontal = True  # start with a horizontal ship

    #Puts the ship in the center of the grid
    line_pos_x = x_size // 2
    line_pos_y = (y_size - size) // 2

    while True: # runs until the ship position is confirmed or the player cancels
        temp_grid = add_line_to_grid(grid, line_pos_x, line_pos_y, size, horizontal)  # a version of the grid that shows the area the ship will be placed
        clearAndPass() # clear terminal
        print("Move your new ship!")
            
        display_grid(temp_grid) # print the grid

        move = input("Move (W=up, A=left, S=down, D=right, R=rotate, C=confirm, Q=cancel): ").upper() #gets the users input and converts it to an uppercase char
        if move == 'W' and line_pos_x > 0:  #if input is w and the player wont go out of bounds, move the line up
            line_pos_x -= 1 #moves the line up
        elif move == 'S' and (line_pos_x < x_size - 1 if horizontal else line_pos_x + size - 1 < x_size - 1): #if input is s and the player wont go out of bounds, move the line down
            line_pos_x += 1 #moves the line down
        elif move == 'A' and line_pos_y > 0: #if input is a and the player wont go out of bounds, move the line left
            line_pos_y -= 1 #moves the line left
        elif move == 'D' and (line_pos_y < y_size - 1 if not horizontal else line_pos_y + size - 1 < y_size - 1): #if input is d and the player wont go out of bounds, move the line right
            line_pos_y += 1 #moves the line right
        elif move == 'R': #if input is r and the player wont go out of bounds, rotate the line
            mid_offset = size // 2  #rotates the line around its center

            if horizontal: #if the line is horizontal, rotate it to be vertical
                new_pos_x = line_pos_x - mid_offset
                new_pos_y = line_pos_y + mid_offset

                if new_pos_x >= 0 and new_pos_x + size <= x_size: #checks to see if the new line position is in bounds
                    line_pos_x = new_pos_x #it is, continue
                    line_pos_y = new_pos_y
                    horizontal = False
                else: #its not, error
                    print("Not enough space to rotate!")
            else: #if the line is vertical, rotate it to be horizontal
                new_pos_x = line_pos_x + mid_offset
                new_pos_y = line_pos_y - mid_offset

                if new_pos_y >= 0 and new_pos_y + size <= y_size: #checks to see if the new line position is in bounds
                    line_pos_x = new_pos_x #it is, continue
                    line_pos_y = new_pos_y
                    horizontal = True
                else: #its not, error
                    print("Not enough space to rotate!")
        elif move == 'C': #if the input is c, confirm the line
            if check_overlap(grid, line_pos_x, line_pos_y, size, horizontal): #checks to make sure this line will not overlap with any other already confirmed lnes
                print("Overlap detected! Move the line to a new position.")
            else:
                grid = add_confirm_to_grid(grid, line_pos_x, line_pos_y, size, horizontal) #add the confirmed line to the grid
                coordinates = get_line_coordinates(line_pos_x, line_pos_y, size, horizontal) #adds the line cords to coordinates
                translated_coords = [grid_coord_to_board_string(y,x) for x,y in coordinates] # translates each coordinate to a board string
                out_ship = Ship(translated_coords) # creates the ship to return
                out_ship.can_split = False # makes it so the ship can't be split again
                print("Ship confirmed at position!") 
                return out_ship  #returns the updated grid and the coordinates of the line
        elif move == 'Q': #if the input is q, cancel placement
            return None  #return none to exit the loop
        else: #invalid input, error
            print("Invalid move! Please use W, A, S, D, R, C, or Q.")
    

# (TEAM2 - JAKE) End


def takeTurn(player: Player, opponent: Player) -> None:
    """
        takeTurn(player: Player)

        Sources: Team authored

        Prints the board and allows the player to take their shot
        
        Returns nothing

        Parameters
            player: a Player instance whose turn it is
    """

    player.printStrikeBoard(opponent) # Print the player's strike board
    print() # Print just a new line for formatting
    player.printBoard(opponent) # Print the player's board
    print(f"\nPlayer {player.number}'s turn!") # Print which player's turn it is

    # (TEAM2 - JAKE)
    splittable_ship = None # initialize possible ship that can be split
    if player.last_enemy_shot is not None: # if the last shot against the current player wasn't a miss
        for ship in player.ships: # loop through al player's ships
            if ship.is_split_possible(player.last_enemy_shot): # check if the ship isn't destroyed and can be split
                splittable_ship = ship # set it as potentially splittable ship
    
    did_split = False
    if splittable_ship: # if a ship can be split
        decision = "" # init player decision
        while decision.upper() not in ("Y", "N", "YES", "NO"): # loop until player makes up their damn mind
            clearAndPass() # looks nicer than having terminal text go on downward forever
            player.printStrikeBoard(opponent) # Print the player's strike board
            print() # Print just a new line for formatting
            player.printBoard(opponent) # Print the player's board
            print(f"\nPlayer {player.number}'s turn!") # Print which player's turn it is
            print(f"Ouch! Looks like one of your ships at {player.last_enemy_shot} got hit for the first time.")
            decision = input("Would you like to break off the hit segment and move the rest of the ship pieces around as a new ship? This will cost a turn. (y/n): ")
        if decision.upper() not in ("Y", "YES"): # if the player didn't choose yes
            splittable_ship.can_split = False # make sure the hit ship can no longer be split
        else: # if the decision was yes
            new_ship_size = splittable_ship.get_split_size() # get the size of the new ship broken off from original
            result = place_split_ship(player, opponent, player.last_enemy_shot, ship, new_ship_size) # let player place the ship
            if result is not None: # if the player didn't cancel placement
                did_split = True
                splittable_ship.abandon() # remove all segments except the hit one from the ship to be split and mark it as destroyed
                player.ships.append(result) # add the new ship to the player's ships array
            splittable_ship.can_split = False # mark the ship, whether it was split or not, as no longer splittable
            clearAndPass() # clear terminal
            player.printStrikeBoard(opponent) # Print the player's strike board
            print() # Print just a new line for formatting
            player.printBoard(opponent) # Print the player's board
            print(f"\nPlayer {player.number}'s turn!") # Print which player's turn it is

    if did_split: # if the player split, their turn is done
        input("Press Enter and pass to the next player...\n") # Print a continue game line to the console
        clearAndPass() # Clear the console for the next player's turn
        input("Next player press enter to continue") # Print a continue game line to the console
        return
    # (TEAM2 - JAKE) End code

            

    enemy_ship_locations = opponent.getShipLocations() # Determine the ship locations of the other player

    while True: # Perform a while loop to avoid duplicate shots
        shot = shootShip(opponent) # Allow the player to choose a coordinate to shoot
        if shot not in player.strike_attempts: # If the shot has not already been taken
            break # Break out of the loop
        print("Shot already taken.\n") # Notify player that the shot was a duplicate
    player.last_strike_was_hit = checkHit(shot, opponent) # Check to see whether the shot was a hit or miss (TEAM2- JAKE) then store value in player object
    player.strike_attempts.append(shot) # Add the shot taken to the player's strike attempts

    input("Press Enter and pass to the next player...\n") # Print a continue game line to the console
    clearAndPass() # Clear the console for the next player's turn
    input("Next player press enter to continue") # Print a continue game line to the console
    '''Team Authored End'''
    
#//start Chat GPT authored
def create_grid(x_size=10, y_size=10): #function that creates a grid filled with '.'
    return [['.' for _ in range(y_size)] for _ in range(x_size)] #fills the grid filled with '.'

def add_line_to_grid(grid, line_pos_x, line_pos_y, size, horizontal=True): #function that adds a line of '#' characters to the grid temporarily to represent a ship
    temp_grid = [row[:] for row in grid]  #used to make a copy of the grid
    for i in range(size): #given a certian size of ship, enter a line into the grid
        if horizontal: #if the line is horizontal, input in this fashion
            temp_grid[line_pos_x][line_pos_y + i] = '#'
        else: #the line is vertical, input in in this fashion
            temp_grid[line_pos_x + i][line_pos_y] = '#'
    return temp_grid #return the updated grid
#//stop Chat GPT authored
#//start team authored
def add_confirm_to_grid(grid, line_pos_x, line_pos_y, size, horizontal=True): #function that adds a line of '+' to the grid to represent a confirmed ship placement
    for i in range(size): #runs for the total size of the ship
        if horizontal: #if the line is horizontal, input in this fashion
            grid[line_pos_x][line_pos_y + i] = '+'
        else: #the line is vertial, input in this fashion
            grid[line_pos_x + i][line_pos_y] = '+'
    return grid #return the updated grid
#//stop team authored
#//start Chat GPT authored
def get_line_coordinates(line_pos_x, line_pos_y, size, horizontal=True): #function that returns each coord the ship is on
    coordinates = [] #initialize a list to hold the ship cords
    for i in range(size): #runs for the total ship size
        if horizontal: #if the ship is horizontal, append in this fashion
            coordinates.append((line_pos_x, line_pos_y + i))
        else: #the ship is vertical, append in this fashion
            coordinates.append((line_pos_x + i, line_pos_y))
    return coordinates #return the finished list

def check_overlap(grid, line_pos_x, line_pos_y, size, horizontal=True): #function that check if a ship is overlapping a previously confirmed ship
    for i in range(size): #check for the entire length of the ship
        if horizontal: #if the ship is horizontal, check in this fashion
            if grid[line_pos_x][line_pos_y + i] != '.': # (TEAM2 - JAKE) if there is not a period in this position, return true -- previously only checked for plus
                return True  #overlap detected
        else: #the ship is horizontal, check in the fashion
            if grid[line_pos_x + i][line_pos_y] != '.': # (TEAM2 - JAKE) if there is not a period in this position, return true -- previously only checked for plus
                return True  #overlap detected
    return False #there is no overlap, return false

def display_grid(grid): #prints out the current grid
    for row in grid: #prints a row
        print(" ".join(row)) #prints each element in a row
    print()

def move_line(grid, size, p1_selection): #moves and places a line of a given size on the grid
    x_size, y_size = len(grid), len(grid[0]) #gives the demensions of the grid to x_size and y_size
    horizontal = True  #start with a horizontal line

    #Puts the line in the center of the grid
    line_pos_x = x_size // 2
    line_pos_y = (y_size - size) // 2

    while True: #runs until the line is confirmed
        temp_grid = add_line_to_grid(grid, line_pos_x, line_pos_y, size, horizontal)  #creates a temproary version of the grid with the current line's position
        clearAndPass() # (TEAM2 - JAKE) this looks so much better
        if p1_selection == False:#checks to see if p1 has confirmed a final board
            print("Player 0 Ship Placement Selection!")#they havent
        else:#me
            print("Player 1 Ship Placement Selection!")#they have
        
        display_grid(temp_grid)#print the grid

        move = input("Move (W=up, A=left, S=down, D=right, R=rotate, C=confirm, Q=quit): ").upper() #gets the users input and converts it to an uppercase char
        if move == 'W' and line_pos_x > 0:  #if input is w and the player wont go out of bounds, move the line up
            line_pos_x -= 1 #moves the line up
        elif move == 'S' and (line_pos_x < x_size - 1 if horizontal else line_pos_x + size - 1 < x_size - 1): #if input is s and the player wont go out of bounds, move the line down
            line_pos_x += 1 #moves the line down
        elif move == 'A' and line_pos_y > 0: #if input is a and the player wont go out of bounds, move the line left
            line_pos_y -= 1 #moves the line left
        elif move == 'D' and (line_pos_y < y_size - 1 if not horizontal else line_pos_y + size - 1 < y_size - 1): #if input is d and the player wont go out of bounds, move the line right
            line_pos_y += 1 #moves the line right
        elif move == 'R': #if input is r and the player wont go out of bounds, rotate the line
            mid_offset = size // 2  #rotates the line around its center

            if horizontal: #if the line is horizontal, rotate it to be vertical
                new_pos_x = line_pos_x - mid_offset
                new_pos_y = line_pos_y + mid_offset

                if new_pos_x >= 0 and new_pos_x + size <= x_size: #checks to see if the new line position is in bounds
                    line_pos_x = new_pos_x #it is, continue
                    line_pos_y = new_pos_y
                    horizontal = False
                else: #its not, error
                    print("Not enough space to rotate!")
            else: #if the line is vertical, rotate it to be horizontal
                new_pos_x = line_pos_x + mid_offset
                new_pos_y = line_pos_y - mid_offset

                if new_pos_y >= 0 and new_pos_y + size <= y_size: #checks to see if the new line position is in bounds
                    line_pos_x = new_pos_x #it is, continue
                    line_pos_y = new_pos_y
                    horizontal = True
                else: #its not, error
                    print("Not enough space to rotate!")
        elif move == 'C': #if the input is c, confirm the line
            if check_overlap(grid, line_pos_x, line_pos_y, size, horizontal): #checks to make sure this line will not overlap with any other already confirmed lnes
                print("Overlap detected! Move the line to a new position.")
            else:
                grid = add_confirm_to_grid(grid, line_pos_x, line_pos_y, size, horizontal) #add the confirmed line to the grid
                coordinates = get_line_coordinates(line_pos_x, line_pos_y, size, horizontal) #adds the line cords to coordinates
                print("Line confirmed at position!") 
                return (grid, coordinates)  #returns the updated grid and the coordinates of the line
        elif move == 'Q': #if the input is q, quit the game
            return (None, None) #return none to exit the loop
        else: #invalid input, error
            print("Invalid move! Please use W, A, S, D, R, C, or Q.")
#//stop Chat GPT authored
def translateCoordinates(ship_tuples: list) -> list:
    """
        translateCoordinates(ship_tuples)

        Sources: Team authored

        Translates ship coordinates from integer tuples to string coordinates, e.g. A3

        Returns a list of lists that contain ship locations in the form of string coordinates

        Parameters
            ship_tuples: a list of lists that contain ship location integer tuples
    """
    all_ship_coordinates = [] # Initialize a list to hold the translated ship coordinates

    for ship in ship_tuples: # For each list of ship locations inside the ships list
        ship_coordinates = [] # Initialize a list to hold individual ships translated coordinates
        for tup in ship: # For each tuple representing a coordinate inside the ship locations
            coordinate = columns[tup[1]] + str_rows[tup[0]] # Convert the integer tuple to a column and row
            ship_coordinates.append(coordinate) # Add the coordinate to the list of ship coordinates
        all_ship_coordinates.append(ship_coordinates) # Add the list of ship coordinates to the list of ships
    
    return all_ship_coordinates # Return the translated ship coordinates

#//start team authored
def goodInput(): #runs until the user inputs a valid number of ships, then returns
    valid_num_ships = ['1','2','3','4','5'] #used to check if user chose the correct number of ships
    goodIn = False #used for while loop to check for a correct input num of ships
    print("Welcome to Battle Ship!") #prints statement 
    while goodIn == False: #runs until we get a good input
        numofShips = input("Choose the number of ships you wish to play with! (1-5): ") #inputted number of ships for the game
        if numofShips in valid_num_ships: #used to break the loop if numofShips in valid_num_ships
            goodIn = True #break loop
            numofShips = int(numofShips) #turns numofShips into an int
        else:
            print("Error! Please input a valid number of ships to start.") #print error and try again
    return numofShips #returns numofShips
#//stop team authored

#//start team and ChatGPT authored
def shipPlacement(nShips): #lets each player choose where they want there ships to be placed, and returns each players confirmed coordinates
    """Handles ship placement in Player vs Player control flow."""
    p1_cords = [] #initializes p1's cords
    p2_cords = [] #initializes p2's cords
    p1_selection = False #sets p1_selection to false
    both_selections = False #sets both_selections to false
    
    while both_selections == False: #runs until both p1 and p2's cords are confirmed
        x_size, y_size = 10, 10 #sets to temp board's width and height
        grid = create_grid(x_size, y_size) #initializes a 10x10 grid
        confirmed_coordinates = []  #temporary list to store a players confirmed cords
        temp_numShips = nShips #creats a temporary number of ships for itiration
        while temp_numShips > 0:  # runs until there are no more ships to place
            grid, line_coordinates = move_line(grid, temp_numShips, p1_selection)  #calls move_line wich returns an updated grid and the cord's of the moved line
            if grid is None:  # checks to see if the player wishes to quit
                print("Game quit.") #print statement
                return  None# return none to quit the game
            confirmed_coordinates.append(line_coordinates)  #input the confirmed coordinates into the confirmed list
            temp_numShips -= 1  #decrement temp_numShips by 1

        #print the final board after all lines have been placed
        print("Final board:")#print statement
        display_grid(grid)#calls display_grid which will print the final grid
        if p1_selection == False:#checks to see if p1's cordinates have been fully confirmed
            for line_coords in confirmed_coordinates:# it hasnt, input coords into p1
                p1_cords.append(line_coords)#adds the cords into p1
            p1_selection = True#sets p1_selection to true
        else:#p1 has already confirmed there cords
            for line_coords in confirmed_coordinates:#input the cords into p2
                p2_cords.append(line_coords)#adds the cords into p2
            both_selections = True#sets both_selections to false to break the while loop
        input('Press Enter and pass to the next player') #move on to the next step
        clearAndPass()
        input('Press Enter to continue')
    return p1_cords, p2_cords #returns both players ship coordinates

# Authored by Drew Meyer
def shipPlacementAI(nShips, player: Player, ai: Ai):
    """
    Allows a human player to place all `n` ships first, then generates the AI's ship placements using Ai.getShipPlacements.
    
    Parameters:
        nShips (int): The number of ships to place.
        player (Player): The human player instance.
        ai (Ai): The AI opponent instance.
        
    Returns:
        tuple: A tuple containing the human player's confirmed coordinates and the AI's confirmed coordinates.
    """
    # Human player ship placement
    human_cords = []  # Initialize the human player's coordinates list
    grid_size = 10  # Define the grid size (10x10)

    grid = create_grid(grid_size, grid_size)  # Initialize the game grid for the human player
    temp_numShips = nShips  # Temporary variable for remaining ships to place
    
    while temp_numShips > 0:  # Continue until all human ships are placed
        grid, line_coordinates = move_line(grid, temp_numShips, p1_selection=True)  # Call move_line to place each ship
        if grid is None:  # If the player chose to quit
            print("Game quit.")  # Print a message
            return None  # Exit the method
        
        human_cords.append(line_coordinates)  # Store the confirmed coordinates for each ship
        temp_numShips -= 1  # Decrement the number of ships left to place
        
    # Display the final board for the human player
    print("Final board for human player:")
    display_grid(grid)

    input("Human player, press Enter to confirm your ship placements and allow AI to place its ships...")  # Continue to AI

    # AI ship placement using the getShipPlacements method
    ai_cords = ai.getShipPlacements(nShips)  # Call Ai.getShipPlacements to generate the AI's ships
    ai_translated_cords = []  # A list to store translated AI coordinates
    
    # Convert AI coordinates to match the grid format
    for ship in ai_cords:
        translated_ship = [grid_coord_to_board_string(x, y) for x, y in ship]
        ai_translated_cords.append(translated_ship)
    
    print("AI has placed its ships.")

    return human_cords, ai_translated_cords  # Return the coordinates for both players


#inspiration from geek for geeks
def clearAndPass():
    # for windows
    if name == 'nt': #name is the name of the os the game is running on
        _ = system('cls') #clear the terminal if on windows
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear') #clear the terminal if on mac or linux

# Authored by original team, adjusted to support AI opponents by Drew Meyer
def main():
    # Drew : Human vs AI Control Flow
    rows = range(1, 11) # Range of rows that should be used for the board. In this case 11 rows, 1 for each number 1-10 and 1 for the header.
    header = '    ' + ' '.join(columns) # Defining the header of the board. # ChatGPT Assisted
    
    while True:
        if_ai = input("Please choose a human (1) or AI opponent (2): ")
        if int(if_ai) == 1:  # input if_ai, 1 = human vs human, 2 = human vs ai
            # Human vs Human Control Flow
            player_zero = Player(0, 'green', header, columns, rows) # Intitializes Human Player 0: Number, color, header, columns, and rows
            player_one = Player(1, 'blue', header, columns, rows)   # Intitializes Human Player 1: Number, color, header, columns, and rows

            p1_confirmed_coordinates = [] #initialize p1's cords
            p2_confirmed_coordinates = [] #initialize p2's cords
            numShips = goodInput() #calls goodInput and returns a valid number of ships for the game.
            
            result = shipPlacement(numShips) #calls shipPlacement and returns two lists containing each players ship coordinates or None if the player decides to quit
            if result is None: #checks if the player quit
                return #quit the game
            p1_confirmed_coordinates, p2_confirmed_coordinates = result
            
            for ship_location in translateCoordinates(p1_confirmed_coordinates): # For each ship in player zero's ship placement coordinate list
                player_zero.ships.append(Ship(ship_location)) # Add each ship to the player's ship list

            for ship_location in translateCoordinates(p2_confirmed_coordinates): # For each ship in player zero's ship placement coordinate list
                player_one.ships.append(Ship(ship_location)) # Add each ship to the player's ship list

            while(True):#runs until checkwin returns false and the game ends and breaks the loop

                # Player 0 turn
                takeTurn(player_zero, player_one) # Player zero takes his turn. Team authored
                if not checkWin(player_zero):  # Check if Player 0 wins
                    break #Game is over so break the loop
                takeTurn(player_one, player_zero) # Player one takes his turn. Team authored
                if not checkWin(player_one):  # Check if Player 1 wins
                    break #Game is over so break the loop
                    #//stop team authored
        elif int(if_ai) == 2: 
            # Human vs AI Control Flow
            while True:  # loop control
                player_zero = Player(0, 'green', header, columns, rows)  # Intitializes Human Player 0: Number, color, header, columns, and rows
                ai_dif = input("Choose AI difficulty: \nChoose 'easy', 'medium' or 'hard'\n")  # Prompt user for difficulty
                if ai_dif != 'easy' and ai_dif != 'medium' and ai_dif != 'hard':
                    print("Invalid difficulty. Try again.")
                else:
                    player_one = Ai(1, 'red', header, columns, rows, difficulty=ai_dif) # Initialize Ai Player 1 with difficulty
                    print("AI difficulty set to ", player_one.difficulty)
                    break
                    
            p1_confirmed_coordinates = [] #initialize p1's cords
            numShips = goodInput() #calls goodInput and returns a valid number of ships for the game.

            # OBTAIN PLAYER 1 SHIP PLACEMENTS, GENERATE AI PLACEMENTS
            # KYLE AND ALEX: Working on this section. Run the current version and start debugging the shipPlacementAI Method
            result = shipPlacementAI(numShips, player=player_zero, ai=player_one) #calls shipPlacement and returns two lists containing each players ship coordinates or None if the player decides to quit

        else:
            print("Please select a valid option: Human (1) vs. AI (2)")

main() #runs the game

