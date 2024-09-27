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
