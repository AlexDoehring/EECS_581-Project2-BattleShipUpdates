""" PROLOGUE COMMENT 


"""

from Ship import Ship
from Player import Player


columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
rows = range(1, 11)
str_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', "10"]
header = '    ' + ' '.join(columns)
player_zero = Player(0)
player_one = Player(1)


def convertTextToColor(text: str, color: str) -> str:
    """
        convertTextToColor(color: str, text: str)

        Function to get the ascii for a string to display it as a given color ('green', 'blue', or 'red')

        Parameters:
            text: a string to  convert the the color specifed by 'color'
            color: a string in ['green', 'blue', 'red'] 

        Returns:
            The 'text' string with the appropriate color code around it
    """
    if (color == 'green'):
        return f'\033[32m{text}\033[0m'
    elif color == 'blue':
        return f'\033[34m{text}\033[0m'
    elif color == 'red':
        return f'\033[31m{text}\033[0m'
    else:
        raise Exception("ERROR: Invalid color string provided")


# Dict to associate players' numbers with their colors 
player_color_dict = {
    0: 'blue',
    1: 'green'
}

def printStrikeBoard(player_num: int, player_strike_attempts: list, opponent_ships: list) -> None: 
    """
        printStrikeBoard(player_num: int, player_strike_attempts: list, opponent_ships: list)

        Prints the board with specified player's strikes on it (misses and hits)

        Parameters:
            player_num: an integer specifying which player's strike board to print
            player_strike_attempts: a list of strings specifying where player has shot
            opponent_ship_locations: a list of strings specifying where the enemy ships are
    """

    # Print column names
    print(convertTextToColor(header, player_color_dict[player_num]))

    # For each row
    for row in rows:
        row_str = f"{row:2} "
        # For each column
        for col in columns:
            cur_pos = col+str(row)
            # If the current position has been shot at by the player
            if cur_pos in player_strike_attempts:
                # Check if that position contains an enemy ship
                if cur_pos in [loc for ship in opponent_ships for loc in ship.locations]:
                    # Print an 'O' in the opponents color for a hit
                    row_str += convertTextToColor(' O', player_color_dict[abs(player_num-1)]) # abs(player_num-1) gets opponents player_num (eg for player 0 -> abs(0-1) = 1)
                # If position does not have an enemy ship, print a red X
                else:
                    row_str += convertTextToColor(' X', 'red')  # Red X
            # If position has not been shot at by player, print a '.' in the color of the player
            else:
                row_str += convertTextToColor(' .', player_color_dict[player_num]) 
        # Print the created string for the current row
        print(convertTextToColor(row_str, player_color_dict[player_num]))




def printBoard(player_num: int, ships: list):
    """
        printBoard(player_num: int, ship_locations: list)

        Prints player's board with their ships on it

        Parameters
            player_num: an int specifying the number of the player
            ships: a list of Ship objects for the player
    """
    # Print column names
    print(convertTextToColor(header, player_color_dict[player_num]))

    # For each row
    for row in rows:
        row_str = f"{row:2} "
        # For each column
        for col in columns:
            # Get current location on board
            cur_pos = col+str(row)
            # If position contains a ship
            if cur_pos in [loc for ship in ships for loc in ship.locations]:
                # Print a '+' 
                row_str += ' +'
            # If position does not contain a ship
            else:
                # Print a '.'
                row_str += ' .'
        print(convertTextToColor(row_str, player_color_dict[player_num]))
        

def checkHit(shot: str, ship_locations: list) -> None: # ADD FUNCTIONALITY FOR SUNK SHIP HERE
    """
        checkHit(shot: str, ship_locations: list)

        Checks whether a shot is a hit or miss and prints the correct message. 
        
        Returns nothing

        Parameters
            shot: a string representing the coordinate of the shot
            ship_locations: a list of Ship locations
    """

    if shot in ship_locations: # Check if the shot hit one of the coordinates held in ship locations
        print("\nHIT!\n") # Print HIT to the console
    else: # If the shot did not hit a ship coordinate
        print("\nMISS!\n") # Print MISS to the console

    # Add condition here to check if ship completely sunk

    
def shootShip(ship_locations: list) -> str: 
    """
        shootShip(ship_locations: list)

        Asks for input coordinates and adds to the shot array to show on the board. Checks if the shot is a hit or miss. 
        
        Returns a string representing the coordinate of the shot taken

        Parameters
            ship_locations: a list of Ship locations
    """

    print("Choose your coordinate to shoot!")

    while True: # Loop to validate the input coordinate
        shot = input("Coordinate: ").upper() # Player inputs coordinate
        if 2 <= len(shot) <= 3 and shot[0] in columns and shot[1] in str_rows: # If the coordinate is 2 or 3 characters long and the first character is a valid column and the second character is a valid row
            if len(shot) == 3 and (shot[1] + shot[2] not in str_rows): # If the coordinate is three characters long and the two characters at the end aren't in the list of valid rows
                continue # Stay in the loop
            break # Break out of the loop

    return shot # Return the coordinate of the shot as a string

    

    
    
def checkWin(): #Check difference between shots and ship locations if all ships are shot return false
    return True
    
def initializeBoard(player_num): # When a player starts setup where they want their ships located NOT DONE
    if player_num == 0: 
        return [
            
        ]
    elif player_num == 1:
        return [
            
        ]
    else:
        raise Exception("ERROR: invalid player_num")


def takeTurn(player: Player) -> None:
    """
        turn(player: Player)

        Prints the board and allows the player to take their shot
        
        Returns nothing

        Parameters
            player: a Player instance whose turn it is
    """

    printStrikeBoard(player.number, player.strike_attempts, player.ships)
    print()
    printBoard(player.number, player.ships)
    print(f"\nPlayer {player.number}'s turn!")

    enemy_ship_locations = player_one.getShipLocations() if player.number == 0 else player_zero.getShipLocations() # Determine the ship locations of the other player
    
    while True: # Perform a while loop to avoid duplicate shots
        shot = shootShip(enemy_ship_locations) # Allow the player to choose a coordinate to shoot
        if shot not in player.strike_attempts: # If the shot has not already been taken
            break # Break out of the loop
        print("Shot already taken.\n") # Notify player that the shot was a duplicate
    checkHit(shot, enemy_ship_locations) # Check to see whether the shot was a hit or miss
    player.strike_attempts.append(shot) # Add the shot taken to the player's strike attempts

    input("Press Enter to continue...\n")
    
#//Ben R start   
def create_grid(x_size=10, y_size=10): #chat gpt
    # Create a grid filled with '.'
    return [['.' for _ in range(y_size)] for _ in range(x_size)]

def add_line_to_grid(grid, line_pos_x, line_pos_y, size, horizontal=True): #chat gpt
    # Add a line of 'size' '#' characters to the grid temporarily
    temp_grid = [row[:] for row in grid]  # Make a copy of the grid
    for i in range(size):
        if horizontal:
            temp_grid[line_pos_x][line_pos_y + i] = '#'
        else:
            temp_grid[line_pos_x + i][line_pos_y] = '#'
    return temp_grid

def add_confirm_to_grid(grid, line_pos_x, line_pos_y, size, horizontal=True): #me
    # Add a line of 'size' '+' characters permanently to the grid
    for i in range(size):
        if horizontal:
            grid[line_pos_x][line_pos_y + i] = '+'
        else:
            grid[line_pos_x + i][line_pos_y] = '+'
    return grid

def get_line_coordinates(line_pos_x, line_pos_y, size, horizontal=True): #chat gpt
    # Generate a list of coordinates for the line
    coordinates = []
    for i in range(size):
        if horizontal:
            coordinates.append((line_pos_x, line_pos_y + i))
        else:
            coordinates.append((line_pos_x + i, line_pos_y))
    return coordinates

def check_overlap(grid, line_pos_x, line_pos_y, size, horizontal=True): #chat gpt
    # Check if the new line overlaps with any '+' on the grid
    for i in range(size):
        if horizontal:
            if grid[line_pos_x][line_pos_y + i] == '+':
                return True  # Overlap detected
        else:
            if grid[line_pos_x + i][line_pos_y] == '+':
                return True  # Overlap detected
    return False  # No overlap

def display_grid(grid): #chat gpt
    # Display the current state of the grid
    for row in grid:
        print(" ".join(row))
    print()

def move_line(grid, size, p1_selection): #chat gpt
    x_size, y_size = len(grid), len(grid[0])
    horizontal = True  # Start with a horizontal line

    # Start the line in the center of the grid
    line_pos_x = x_size // 2
    line_pos_y = (y_size - size) // 2

    while True:
        # Display the grid with the current line
        temp_grid = add_line_to_grid(grid, line_pos_x, line_pos_y, size, horizontal)  # Temporary grid with current line
        if p1_selection == False:#me
            print("Player 1 Ship Placement Selection!")#me
        else:#me
            print("Player 2 Ship Placement Selection!")#me
        display_grid(temp_grid)

        # Get user input for movement
        move = input("Move (W=up, A=left, S=down, D=right, R=rotate, C=confirm, Q=quit): ").upper()

        # Handle movement with bounds checking
        if move == 'W' and line_pos_x > 0:  # Move up
            line_pos_x -= 1
        elif move == 'S' and (line_pos_x < x_size - 1 if horizontal else line_pos_x + size - 1 < x_size - 1):  # Move down
            line_pos_x += 1
        elif move == 'A' and line_pos_y > 0:  # Move left
            line_pos_y -= 1
        elif move == 'D' and (line_pos_y < y_size - 1 if not horizontal else line_pos_y + size - 1 < y_size - 1):  # Move right
            line_pos_y += 1
        elif move == 'R':  # Rotate the line around its center
            mid_offset = size // 2  # Offset from the start to the center of the line

            if horizontal:  # Rotate to vertical
                new_pos_x = line_pos_x - mid_offset
                new_pos_y = line_pos_y + mid_offset

                # Ensure the vertical line fits in bounds
                if new_pos_x >= 0 and new_pos_x + size <= x_size:
                    line_pos_x = new_pos_x
                    line_pos_y = new_pos_y
                    horizontal = False
                else:
                    print("Not enough space to rotate!")
            else:  # Rotate to horizontal
                new_pos_x = line_pos_x + mid_offset
                new_pos_y = line_pos_y - mid_offset

                # Ensure the horizontal line fits in bounds
                if new_pos_y >= 0 and new_pos_y + size <= y_size:
                    line_pos_x = new_pos_x
                    line_pos_y = new_pos_y
                    horizontal = True
                else:
                    print("Not enough space to rotate!")
        elif move == 'C':  # Confirm and save current line
            if check_overlap(grid, line_pos_x, line_pos_y, size, horizontal):
                print("Overlap detected! Move the line to a new position.")
            else:
                grid = add_confirm_to_grid(grid, line_pos_x, line_pos_y, size, horizontal)
                coordinates = get_line_coordinates(line_pos_x, line_pos_y, size, horizontal)
                print("Line confirmed at position!")
                return (grid, coordinates)  # Return the updated grid and the coordinates of the line
        elif move == 'Q':  # Quit the game
            print("Game ended.")
            return (None, None)  # Return None to exit the loop
        else:
            print("Invalid move! Please use W, A, S, D, R, C, or Q.")
#//Ben R end         
def main():
    
    #//Ben R start
    p1_confirmed_coordinates = [] #//me
    p2_confirmed_coordinates = [] #me
    p1_selection = False #me
    both_selections = False #me
    valid_num_ships = ['1','2','3','4','5'] #used to check if user chose the correct number of ships
    goodInput = False #used for while loop to check for a correct input num of ships
    
    #choosing the number of ships 
    print("Welcome to Battle Ship!")
    while goodInput == False: #runs until we get a good input
        numShips = input("Choose the number of ships you wish to play with! (1-5): ") #inputted number of ships for the game
        if numShips in valid_num_ships: #used to break the loop if numShips in valid_num_ships
            goodInput = True #break loop
            numShips = int(numShips) #now we want it to be a type int for later
        else:
            print("Error! Please input a valid number of ships to start.") #print error and try again
    #//Ben R end
    
    #//Ben R start ship placement
    while both_selections == False: #me
        # Initialize an empty grid
        x_size, y_size = 10, 10 #chatgpt
        grid = create_grid(x_size, y_size)#chatgpt
        confirmed_coordinates = []  # List to store the coordinates of confirmed lines
        temp_numShips = numShips#me
        while temp_numShips > 0:  # Continue until the line size reaches 0#chatgpt
            result = move_line(grid, temp_numShips, p1_selection)  # Pass the existing grid to keep confirmed lines
            grid, line_coordinates = result#chatgpt
            if grid is None:#chatgpt
                break  # Exit the loop if the player quits
            confirmed_coordinates.append(line_coordinates)  # Save the coordinates of the confirmed line
            temp_numShips -= 1  # Decrease the size of the line after each confirmation

        # Final board after all lines have been placed
        print("Final board:")#me
        display_grid(grid)#me
        if p1_selection == False:#me
            for line_coords in confirmed_coordinates:#me
                p1_confirmed_coordinates.append(line_coords)#me
            p1_selection = True#me
        else:#me
            for line_coords in confirmed_coordinates:#me
                p2_confirmed_coordinates.append(line_coords)#me
            both_selections = True#me
        input('Press anything to continue: ') #me
    #//Ben R end      
    while(checkWin()):

        # Initalize
        player_zero.ships = initializeBoard(0)

        player_one.ships = initializeBoard(1)

        # Player 0 turn
        takeTurn(player_zero)
        
        # Player 1 turn
        takeTurn(player_one)
    
    
main()

