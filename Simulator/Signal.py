import enum


class Directions(enum.Enum):
    RIGHT = 1
    LEFT = 2


class Signal:
    """Signal class - objects which are inserted into carrier by stations"""
    def __init__(self, signature, starting_pos, direction):
        self.position = starting_pos
        self.signature = signature
        self.direction = direction

    def perform_step(self):
        # depending on where the signal is going change its position
        if self.direction == Directions.RIGHT:
            self.position += 1
        elif self.direction == Directions.LEFT:
            self.position -= 1





