from Player import Player

class Ai(Player):
    def __init__(self, number: int, color: str, header: str, columns: list, rows: list, difficulty: str):
        super().__init__(number, color, header, columns, rows)
        self.difficulty = difficulty  # Add difficulty level for AI

    def make_move(self):
        if self.difficulty == 'easy':
            # Implement easy AI move logic (random move)
            pass
        elif self.difficulty == 'medium':
            # Implement medium AI move logic (random until hit, then adjacent)
            pass
        elif self.difficulty == 'hard':
            # Implement hard AI move logic (knows all ship locations)
            pass
