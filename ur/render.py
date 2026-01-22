from ur.board import Board

CELL_W = 5
CELL_H = 3


def cell_block(cell):
    """
    Возвращает список из 3 строк (высота клетки)
    """
    cell_id_str = str(cell.id) if hasattr(cell, 'id') else "  "
    if cell.rosette:
        top = f"**{cell_id_str}**"
        mid = "*   *"
        bot = "*****"
    else:
        top = f"  {cell_id_str}  "
        mid = "     "
        bot = "     "

    # если есть фишка — кладём в центр
    if cell.occupants:
        symbol = cell.occupants[0]
        mid = f"* {symbol} *" if cell.rosette else f"  {symbol}  "

    return [top, mid, bot]


def empty_block():
    return ["     ", "     ", "     "]


def render_board(board: Board, player_x, player_o):
    home_x = player_x.pieces.count(-1)
    goal_x = player_x.pieces.count(14)

    home_o = player_o.pieces.count(-1)
    goal_o = player_o.pieces.count(14)
    print()
    print((" " * 19) + "X" * home_x + "." * (7 - home_x) + (" " * 11) + "X" * goal_x + "." * (7 - goal_x))
    print((" " * 19) + "Home" + (" " * 14) + "Goal")

    # Верхняя часть доски
    print("┌─────┬─────┬─────┬──↓──┐           ┌──↑──┬─────┐")

    for h in range(3):
        line = "│"
        for c in range(4):
            block = cell_block(board.grid[0][c])
            line += block[h] + "│"

        line += "           │"
        for c in range(6, 8):
            block = cell_block(board.grid[0][c])
            line += block[h] + "│"

        print(line)

    # Верхняя середина доски
    print("├──↓──┼─────┼─────┼─────┼─────┬─────┼─────┼──↑──┤")

    for h in range(3):
        line = "│"
        for c in range(8):
            block = cell_block(board.grid[1][c])
            line += block[h] + "│"
        print(line)

    # Нижняя середина доски
    print("├──↑──┼─────┼─────┼─────┼─────┴─────┼─────┼──↓──┤")

    for h in range(3):
        line = "│"
        for c in range(4):
            block = cell_block(board.grid[2][c])
            line += block[h] + "│"

        line += "           │"
        for c in range(6, 8):
            block = cell_block(board.grid[2][c])
            line += block[h] + "│"

        print(line)

    # Нижняя часть доски
    print("└─────┴─────┴─────┴──↑──┘           └──↓──┴─────┘")
    print((" " * 19) + "Home" + (" " * 14) + "Goal")
    print((" " * 19) + "O" * home_o + "." * (7 - home_o) + (" " * 11) + "O" * goal_o + "." * (7 - goal_o))
    print()