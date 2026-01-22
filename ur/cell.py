class Cell:
    def __init__(self, cid: str, rosette: bool = False):
        self.id = cid # A, B, C ...
        self.rosette = rosette # True / False
        self.occupants = [] # X, O

    def is_empty(self) -> bool:
        return len(self.occupants) == 0