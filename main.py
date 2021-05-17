from typing import List, Dict


class Game:
    def __init__(self):
        self.positions: List[List[str]] = [[' ', ' ', ' '],
                                           [' ', ' ', ' '],
                                           [' ', ' ', ' ']]
        self.turn: bool = False
        self.coords: Dict[str, List[int]] = {
            'A1': [0, 0],
            'A2': [1, 0],
            'A3': [2, 0],
            'B1': [0, 1],
            'B2': [1, 1],
            'B3': [2, 1],
            'C1': [0, 2],
            'C2': [1, 2],
            'C3': [2, 2],
        }
        self.game_won: bool = False
        self.filled: bool = False

    def start_game(self):
        while not self.game_won or self.filled:
            self.show_board()
            proper_move = False
            while not proper_move:
                move = self.get_input().upper()
                try:
                    if len(move) > 2:
                        raise MarkerError
                    self.mark_coord(self.get_coords(move))
                    proper_move = True
                except (MarkerError, KeyError, IndexError) as err:
                    self.show_board()
                    print(f'({move}) Invalid move')
                    continue
            self.game_won = self.check_win()
            self.filled = self.check_filled()
            if self.game_won or self.filled:
                break
            self.switch_turn()
        winner = 'X won!' if not self.turn else 'O won!'
        self.show_board()
        if self.game_won:
            print(winner)
        elif self.filled:
            print('Tie game')
        else:
            print('Weird')
            self.show_board()

    # Helper Methods
    def get_input(self):
        return input('Enter a move (ex: A1): ')

    def show_board(self):
        print('  A | B | C ')
        for h in range(3):
            row_string = f'{h + 1}'
            for w in range(3):
                row_string += f' {self.positions[h][w]} |' if w != 2 else f' {self.positions[h][w]} '
            print(row_string)
            print('  ----------' if h != 2 else '')

    def switch_turn(self):
        new_turn = not self.turn
        self.turn = new_turn

    def get_coords(self, move: str):
        xy_coord = move[0] + move[1]
        return self.coords[xy_coord]

    def mark_coord(self, coords: List[int]):
        [x, y] = coords
        marker = self.positions[x][y]
        if marker != ' ':
            raise MarkerError
        marker = 'X' if not self.turn else 'O'
        self.positions[x][y] = marker

    # Game Checks
    def check_filled(self):
        for row in self.positions:
            if not all(val != ' ' for val in row):
                return False
        return True

    def check_win(self):
        positions = self.positions
        for row_idx, row in enumerate(positions):
            # Check horizontal
            horizontal_filled = self.check_horizontals(row)
            if horizontal_filled:
                return True
            if row_idx != 0:
                continue
            # Check verticals
            vertical_filled = self.check_verticals(row_idx, row, positions)
            if vertical_filled:
                return True
        # Check diagonals
        return self.check_diagonals(positions)

    def check_horizontals(self, row: List[str]):
        if all(marker == row[0] and row[0] != ' ' for marker in row):
            return True
        return False

    def check_verticals(self, row_idx: int, row: List[str], positions: List[List[str]]):
        for column_idx, column_val in enumerate(row):
            sec_col = positions[row_idx + 1][column_idx]
            third_col = positions[row_idx + 2][column_idx]
            if column_val == sec_col and sec_col == third_col and column_val != ' ':
                return True
        return False

    def check_diagonals(self, positions: List[List[str]]):
        first_diagonal = [positions[0][0], positions[1][1], positions[2][2]]
        sec_diagonal = [positions[0][2], positions[1][1], positions[2][0]]
        first_val = first_diagonal[0]
        sec_val = sec_diagonal[0]
        first_diag_check = all(marker == first_val and first_val != ' ' for marker in first_diagonal)
        sec_diag_check = all(marker == sec_val and sec_val != ' ' for marker in sec_diagonal)
        if first_diag_check or sec_diag_check:
            return True
        return False


class MarkerError(Exception):
    pass


def start_game():
    game = Game()
    game.start_game()


if __name__ == '__main__':
    start_game()
