from ur.board import Board
from ur.player import Player
from ur.dice import roll_dice
from ur.board_layout import PATH_X, PATH_O, ROSETTES
from ur.render import render_board

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("X"), Player("O")]
        self.current = 0  # индекс текущего игрока

    def switch_player(self):
        self.current = 1 - self.current

    def move_piece(self, player: Player, piece_idx: int, steps: int):
        """
        Перемещает фишку игрока по его PATH (PATH_X или PATH_O),
        учитывает Goal, выбивание противника, защиту розеток и доп ход
        """
        path = PATH_X if player.symbol == "X" else PATH_O

        pos = player.pieces[piece_idx]
        new_pos = pos + steps if pos >= 0 else steps - 1  # из Home = -1

        # Если выходит за пределы пути, Goal требуется точный бросок
        if new_pos == len(path):
            # фишка вышла
            if pos >= 0:
                old_cell = self.board.get_cell(path[pos])
                old_cell.occupants.remove(player.symbol)

            player.pieces[piece_idx] = 14
            print("Фишка дошла до финиша!")
            return False

        if new_pos > len(path):
            print("Нужен точный бросок!")
            return False

        new_cell_id = path[new_pos]
        target_cell = self.board.get_cell(new_cell_id)

        # Нельзя ходить на клетку, если там своя фишка
        if any(o == player.symbol for o in target_cell.occupants):
            print("Нельзя встать на свою фишку!")
            return False

        # Обработка захвата
        if target_cell.occupants:
            occ = target_cell.occupants[0]
            if occ != player.symbol and new_cell_id not in ROSETTES:
                for p in self.players:
                    if p.symbol == occ:
                        for i, pos in enumerate(p.pieces):
                            opp_path = PATH_X if occ == "X" else PATH_O
                            if pos >= 0 and opp_path[pos] == new_cell_id:
                                p.pieces[i] = -1
                                break
                target_cell.occupants.clear()

        # Перемещаем фишку
        target_cell.occupants.append(player.symbol)

        # Очищаем старую клетку
        if pos >= 0:
            old_cell = self.board.get_cell(path[pos])
            if player.symbol in old_cell.occupants:
                old_cell.occupants.remove(player.symbol)

        player.pieces[piece_idx] = new_pos

        # Доп ход при попадании на розетку
        if new_cell_id in ROSETTES:
            print("Розетка! Дополнительный ход!")
            return True

        return False

    def play_turn(self):
        player = self.players[self.current]
        roll = roll_dice()
        print(f"\nИгрок {player.symbol} бросил: {roll}")

        if roll == 0:
            print("Ход пропущен")
            self.switch_player()
            return

        path = PATH_X if player.symbol == "X" else PATH_O

        # Возможность ввести новую фишку из Home
        enterable = roll - 1 < len(path) and roll > 0 and player.pieces.count(-1) > 0
        movable = player.get_movable_pieces(roll, path, self.board)

        if not enterable and not movable:
            print("Нет возможных ходов")
            self.switch_player()
            return

        # Список опций
        options = []
        if enterable:
            options.append("new")
        for i in movable:
            options.append(i)

        print("Доступные ходы:")

        for i in movable:
            pos = player.pieces[i]
            start = "Home" if pos == -1 else path[pos]

            new_pos = pos + roll if pos >= 0 else roll - 1
            end = "Goal" if new_pos == len(path) else path[new_pos]

            suffix = " (розетка)" if end in ROSETTES else ""
            print(f"[{i}] {start} → {end}{suffix}")

        while True:
            choice = input("Выберите ход (new или номер): ")
            if choice.isdigit() and int(choice) in movable:
                piece_idx = int(choice)
                extra = self.move_piece(player, piece_idx, roll)
                break
            else:
                print("Неверный выбор!")

        render_board(self.board, self.players[0], self.players[1])

        if not extra:
            self.switch_player()