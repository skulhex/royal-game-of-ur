from ur.game import Game

def main():
    game = Game()

    while True:
        game.play_turn()
        for p in game.players:
            if p.has_won():
                print(f"Игрок {p.symbol} выиграл!")
                return

if __name__ == "__main__":
    main()