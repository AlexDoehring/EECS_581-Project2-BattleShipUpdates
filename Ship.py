""" 
    Program name: Ship.py
    Description: defines the ship type
    Inputs: a list of locations
    Outputs: a ship object 
    Sources of code: None
    Authors: Connor Bennudriti, Brinley Hull, Gianni Louisa, Kyle Moore, Ben Renner
    Creation Date: 9/7/2024
"""

class Ship:
    def __init__(self, locations: list):
        """
            __init__(self, locations: list)

            Sources: Team authored

            Initalized the Ship class

            Returns None

            Parameters:
                locations: A list of board locations where ship segments are located
        """
        self.locations = locations # A list of board locations where ship segments are located
        self.hit_segments = [] # A list containing the locations of ship segments that have been hit
        self.destroyed: bool = False # A bool to sinify if the ship has been destroyed (all segments hit)

        """
            (TEAM2 - JAKE) Added for the new feature where players can "move" their ships after being hit once

            If a ship has not been hit before, it can abandon the hit segment and move the rest of its segments
            (as a smaller ship) to a different place on the board.

            These newly created ships cannot split, and if a ship is hit once and a player decides not to split,
            it cannot be split later.
        """
        # initialize to True by default (unless it's a length 1 ship), set False within program if necessary
        self.can_split = len(self.locations) > 1

    # (TEAM2 - JAKE) get size of split ship
    def get_split_size(self) -> int:
        return len(self.locations) - 1 # we abandon only one segment of the ship

    # (TEAM2 - JAKE) used to abandon part of a ship and remove the segments that weren't hit
    # needed for splitting a ship and moving the rest elsewhere
    def abandon(self):
        self.locations = self.hit_segments # remove all segments except the 1 hit segment
        self.destroyed = True # count this as a destroyed ship

    # (TEAM2 - JAKE) check if a hit was in a ship's segments and if a ship has the ability to split based on that hit
    # hit is a string containing the coordinates of a hit, eg "C6"
    def is_split_possible(self, hit: str) -> bool:
        if not self.can_split or self.destroyed: # if it's destroyed or can't split, exit immediately
            return False
        else: # otherwise, check if the hit was in one of the ship's hit segments (should already be set when this function is run)
            return hit in self.hit_segments


