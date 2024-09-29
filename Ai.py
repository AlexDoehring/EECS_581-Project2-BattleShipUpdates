"""
    Program name: Ai.py
    Description: Creates a class to hold Ai opponent object information.
                 Subclass of Player.
    Inputs:
    * super().__init__
        -number: (int) Player's identification number.
        -color: (str) The color associated with the player, should be either 'blue' or 'green'.
        -header: (str) Header string representing column labels for the game board.
        -columns: (list of str) List of strings representing the columns on the board.
        -rows: (list of int) List of integers representing the row numbers on the board.
    * __init__
        - difficulty: (str) Level of difficulty for Ai opponent (easy, medium, hard)
    Outputs:
    * getShipPlacements
        - Returns list of randomly placed valid ship locations
    
    Authors: Jake Bernard, Drew Meyer
    Creation Date: 9/28/2024
"""

from Player import Player
import random

columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

class Ai(Player):
    """Subclass of Player, represents Ai opponent."""
    def __init__(self, number: int, color: str, header: str, columns: list, rows: list, difficulty: str):
        super().__init__(number, color, header, columns, rows)
        self.difficulty = difficulty  # Add difficulty level for AI

    #Might need to add more parameters, i.e. opponents board for hard difficulty, last shot for medium difficulty
    def shootShip(self, opponent):
        if self.difficulty == 'easy':      # Easy difficulty (continuous random shots)
            col = columns[random.randint(0, 9)]
            row = str(random.randint(1, 10))
            shot = row + col
            self.strike_attempts.append(shot)
            return shot
        elif self.difficulty == 'medium':  # Medium difficulty (random until hit, then adjacent)
            if self.last_strike_was_hit:
                last_row, last_col = self.last_hit[0], self.last_hit[1:]
                possible_shots = []
            
                # Check adjacent cells (up, down, left, right)
                if last_row > 1:  # Up
                    possible_shots.append((row - 1, col))
                if last_row < len(self.rows):  # Down
                    possible_shots.append((row + 1, col))
                if last_col != 'A':  # Left
                    possible_shots.append((row, chr(ord(col) - 1)))
                if last_col != 'J':  # Right
                    possible_shots.append((row, chr(ord(col) + 1)))
                
                # Filter out the shots already attempted
                for shot in possible_shots:
                    if shot in self.strike_attempts:
                        possible_shots.remove(shot)
                        
                return random.choice(possible_shots)
                
            else:
                col = columns[random.randint(0, 9)]
                row = str(random.randint(1, 10))
                shot = row + col
                self.strike_attempts.append(shot)
                return shot
        elif self.difficulty == 'hard':    # Hard difficulty (knows all ship locations)
            for coord in opponent.getShipLocations():
                if coord not in self.strike_attempts:
                    self.strike_attempts.append(coord) #add coordinate to strike attempt
                    return coord #return shot

    def getShipPlacements(self, size: int) -> list:
        """Function to get random placement of ships."""
        # init ships array
        ships = []
        # loop for each ship size
        for s in range(0,size):
            # has a suitable placement been found
            found = False
            # if not, we randomly generate a spot and orientation and check if it works
            # could get insanely unlucky and it loops forever, but likely not to happen
            while not found:
                cur = []     # current set of coordinates for the ship's segments
                horizontal = bool(random.randint(0,1)) # randomly set it to be horizontal or vertical
                x = random.randint(0, 9) if not horizontal else random.randint(0, 9 - s)  # set x position somewhere on grid
                y = random.randint(0, 9) if horizontal else random.randint(0, 9 - s)      # set y position somewhere on grid
                
                faulty = False               # Check for bad placement
                for ship in ships:           # loop through all set ships
                    for i in range(s + 1):   # traverse along the ship's length
                        if horizontal:       # if horizontal, move horizontally (positive x)
                            if [x + i, y] in ship:  # if this segment exists on a ship
                                faulty = True       # it's not a good pick, break and choose a new spot
                                break
                        else:                       # if it's vertical, we move vertically along the ship (positive y
                            if [x, y + i] in ship:  # check each segment
                                faulty = True       # if it exists in another ship, it's a collision
                                break               # break out of nested loop     
                    if faulty:           # if it wasn't fault, a good position was found
                        break
                
                found = not faulty 
                if found:                  # if a good position was found
                    for i in range(s + 1): # loop through ship along length
                        if horizontal:     # if horizontal
                            cur.append([x + i, y])  # add segments horizontally
                        else:              # otherwise
                            cur.append([x, y + i])  # add segments to current ship vertically
                    ships.append(cur)       # add the new ship to list of ships
        return ships    # return all the ships
