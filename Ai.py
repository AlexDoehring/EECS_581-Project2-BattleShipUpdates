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

    def getShipPlacements(self, size: int) -> list:
        ships = []
        for s in range(0,size):
            found = False
            while not found:
                cur = []
                horizontal = bool(random.randint(0,1))
                x = random.randint(0, 9) if not horizontal else random.randint(0, 9 - s + 1)
                y = random.randint(0, 9) if horizontal else random.randint(0, 9 - s + 1)
                faulty = False
                for ship in ships:
                    for i in range(s + 1):
                        if horizontal:
                            if [x + i, y] in ship:
                                faulty = True
                                break
                        else:
                            if [x, y + i] in ship:
                                faulty = True      
                    if faulty:
                        break
                found = not faulty
                if found:
                    for i in range(s + 1):
                        if horizontal:
                            cur.append([x + i, y])
                        else:
                            cur.append([x, y + i])
                    ships.append(cur)
        return ships
