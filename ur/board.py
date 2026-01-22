from ur.cell import Cell
from ur.board_layout import BOARD_GRID, ROSETTES

class Board:
    def __init__(self):
        self.grid = []
        self.cells = {}

        for row in BOARD_GRID:
            grid_row = []
            for cid in row:
                if cid is None:
                    grid_row.append(None)
                else:
                    cell = Cell(cid, rosette=(cid in ROSETTES))
                    self.cells[cid] = cell
                    grid_row.append(cell)
            self.grid.append(grid_row)

    def get_cell(self, cid: str) -> Cell:
        return self.cells[cid]
