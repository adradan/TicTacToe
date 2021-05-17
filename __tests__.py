import unittest
from main import Game, MarkerError


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()


class TestMethods(TestGame):
    def test_switch_turn(self):
        turn = self.game.turn
        self.game.switch_turn()
        new_turn = self.game.turn
        self.assertNotEqual(turn, new_turn, 'Turn not switched')

    def test_get_coords(self):
        [x, y] = self.game.get_coords('A1')
        self.assertEqual(f'{x}{y}', '00', 'Wrong Coord for A1')

    def test_success_x_marker(self):
        self.game.turn = False
        current_marker = self.game.positions[0][0]
        self.game.mark_coord([0, 0])
        new_marker = self.game.positions[0][0]
        self.assertNotEqual(current_marker, new_marker)
        self.assertEqual(new_marker, 'X')

    def test_success_o_marker(self):
        self.game.turn = True
        current_marker = self.game.positions[0][0]
        self.game.mark_coord([0, 0])
        new_marker = self.game.positions[0][0]
        self.assertNotEqual(current_marker, new_marker)
        self.assertEqual(new_marker, 'O')

    def test_failure_x_marker(self):
        self.game.turn = False
        self.game.positions[0][0] = 'X'
        self.assertRaises(MarkerError, self.game.mark_coord, [0, 0])

    def test_not_filled(self):
        is_filled = self.game.check_filled()
        self.assertFalse(is_filled)

    def test_is_filled(self):
        for row_idx in range(len(self.game.positions)):
            set_horizontal(self.game, row_idx)
        is_filled = self.game.check_filled()
        self.assertTrue(is_filled)

    def test_some_filled(self):
        for row_idx in range(len(self.game.positions)):
            set_horizontal(self.game, row_idx)
        self.game.positions[0][1] = ' '
        is_filled = self.game.check_filled()
        self.assertFalse(is_filled)


class TestWinConditions(TestGame):
    def test_win_empty(self):
        win = self.game.check_win()
        self.assertFalse(win)

    def test_first_horizontal_win(self):
        set_horizontal(self.game, 0)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_sec_horizontal_win(self):
        set_horizontal(self.game, 1)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_third_horizontal_win(self):
        set_horizontal(self.game, 2)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_first_vertical_win(self):
        set_vertical(self.game, 0)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_sec_vertical_win(self):
        set_vertical(self.game, 1)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_third_vertical_win(self):
        set_vertical(self.game, 2)
        win = self.game.check_win()
        self.assertTrue(win)

    def test_two_filled_lose(self):
        set_horizontal(self.game, 0)
        self.game.positions[0][1] = ' '
        win = self.game.check_win()
        self.assertFalse(win)


def set_horizontal(game: Game, row_idx: int):
    for idx, elem in enumerate(game.positions[row_idx]):
        game.positions[row_idx][idx] = 'X'


def set_vertical(game: Game, idx: int):
    for row_idx, row in enumerate(game.positions):
        for col_idx, col in enumerate(row):
            if col_idx != idx:
                continue
            game.positions[row_idx][col_idx] = 'X'
