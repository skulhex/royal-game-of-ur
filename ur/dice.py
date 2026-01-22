import random

def roll_dice() -> int:
    """
    Бросок 4 монет: решка=1, орёл=0
    """
    return sum(random.choice([0,1]) for _ in range(4))