from Player import Player
import random

columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

class Ai(Player):
    def __init__(self, number: int, color: str, header: str, columns: list, rows: list, difficulty: str):
        super().__init__(number, color, header, columns, rows)
        self.difficulty = difficulty  # Add difficulty level for AI

    #Might need to add more parameters, i.e. opponents board for hard difficulty, last shot for medium difficulty
    def shootShip(self):
        if self.difficulty == 'easy':
            col = columns[random.randint(0, 9)]
            row = str(random.randint(1, 10))
            return row + col
        elif self.difficulty == 'medium':
            # Implement medium AI move logic (random until hit, then adjacent)
            pass
        elif self.difficulty == 'hard':
            # Implement hard AI move logic (knows all ship locations)
            pass

    # Function to get random placement of ships
    def getShipPlacements(self, size: int) -> list:
        # init ships array
        ships = []
        # loop for each ship size
        for s in range(0,size):
            # has a suitable placement been found
            found = False
            # if not, we randomly generate a spot and orientation and check if it works
            # could get insanely unlucky and it loops forever, but likely not to happen
            while not found:
                # current set of coordinates for the ship's segments
                cur = []
                # randomly set it to be horizontal or vertical
                horizontal = bool(random.randint(0,1))
                # set its x position to never be somewhere where it would go off the grid
                x = random.randint(0, 9) if not horizontal else random.randint(0, 9 - s)
                # set its y to never go off the grid
                y = random.randint(0, 9) if horizontal else random.randint(0, 9 - s)
                # is the placement bad?
                faulty = False
                # loop through all set ships
                for ship in ships:
                    # traverse along the ship's length
                    for i in range(s + 1):
                        # if it's horizontal, move horizontally (positive x)
                        if horizontal:
                            # if this segment already exists on a ship
                            if [x + i, y] in ship:
                                # it's not a good pick, break and choose a new spot
                                faulty = True
                                break
                        # if it's vertical, we move vertically along the ship (positive y
                        else:
                            # check each segment
                            if [x, y + i] in ship:
                                # if it exists in another ship, it's a collision
                                faulty = True
                                break 
                    # break out of nested loop     
                    if faulty:
                        break
                # if it wasn't fault, a good position was found
                found = not faulty
                # if a good position was found
                if found:
                    # loop through ship along length
                    for i in range(s + 1):
                        # if it's horizontal
                        if horizontal:
                            # add segments horizontally
                            cur.append([x + i, y])
                        # otherwise
                        else:
                            # add segments to current ship vertically
                            cur.append([x, y + i])
                    # add the newly made ship to the list of ships
                    ships.append(cur)
        # return all the ships
        return ships
