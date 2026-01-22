from ur.board_layout import CENTRAL_ROSETTE

class Player:
    def __init__(self, symbol: str):
        self.symbol = symbol        # 'X' или 'O'
        self.pieces = [-1] * 7      # позиции 7 фишек: -1 = Home, 0-13 = на пути, 14 = Goal

    def finished_pieces(self) -> int:
        return sum(1 for p in self.pieces if p == 14)

    def has_won(self) -> bool:
        return self.finished_pieces() == 7

    def get_movable_pieces(self, roll: int, path: list, board):
        movable = []

        for i, pos in enumerate(self.pieces):
            if pos == 15:
                continue  # фишка уже в Goal

            new_pos = pos + roll if pos >= 0 else roll - 1

            # выход за путь → нельзя
            if new_pos > len(path):
                continue

            # точный выход в Goal
            if new_pos == len(path):
                movable.append(i)
                continue

            target_cell = board.get_cell(path[new_pos])

            # нельзя вставать на свою фишку
            if self.symbol in target_cell.occupants:
                continue

            # нельзя выбивать на центральной розетке
            if (
                    target_cell.occupants
                    and path[new_pos] == CENTRAL_ROSETTE
            ):
                continue

            movable.append(i)

        return movable