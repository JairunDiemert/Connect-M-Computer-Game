#!/usr/bin/env python3
'''
Test Suite for Connect M Game.

This module contains unit tests for both the game logic in the ConnectMGame class
and the CLI functionality in main.py.

@author Jairun Diemert
@date 2025-02-24
@info CAP 4601 Project 1: Adversarial Search Spring 2025
'''

import unittest  # Import the unittest framework.
import subprocess  # Import subprocess to run CLI commands.
import sys  # Import sys for access to the Python interpreter.
from connectM_game import ConnectMGame  # Import the ConnectMGame class for testing.

class TestConnectMGame(unittest.TestCase):
	'''
	Unit tests for the ConnectMGame class.

	These tests cover game logic including move validation, win and draw detection,
	board evaluation, and the alpha-beta search algorithm.
	'''

	def setUp(self):
		'''
		Set up a new game instance for each test.

		This method is run before every test method to ensure a fresh board.

		@return None
		'''
		# Define a board size of 5 and winning condition of 4.
		self.board_size = 5
		self.connect_m = 4
		# Create a new ConnectMGame instance with the human moving first.
		self.game = ConnectMGame(self.board_size, self.connect_m, True)

	def test_is_valid_move(self):
		'''
		Test that valid moves are recognized and invalid moves are rejected.

		@return None
		'''
		# On an empty board, every column should be valid.
		for col in range(self.board_size):
			self.assertTrue(self.game.isValidMove(col), f'Column {col} should be valid on an empty board.')

		# Fill an entire column (e.g., column 2) and ensure it becomes invalid.
		col_to_fill = 2
		for _ in range(self.board_size):
			move_made = self.game.makeMove(col_to_fill, self.game.human_symbol)
			self.assertTrue(move_made, 'Move should be successful.')
		self.assertFalse(self.game.isValidMove(col_to_fill), 'Column should be full and invalid for a move.')

	def test_make_move(self):
		'''
		Test that a move places a disk in the correct position on the board.

		@return None
		'''
		# Make a move in column 1.
		col = 1
		self.assertTrue(self.game.makeMove(col, self.game.human_symbol), 'Move should be successful.')
		# The disk should appear in the bottom row of column 1.
		self.assertEqual(self.game.board[self.board_size - 1][col], self.game.human_symbol,
			'The disk should be placed at the bottom row.')

	def test_horizontal_win(self):
		'''
		Test detection of a horizontal win condition.

		@return None
		'''
		# Manually fill a horizontal segment on the bottom row for the human.
		row = self.board_size - 1
		for col in range(self.connect_m):
			self.game.board[row][col] = self.game.human_symbol
		# Check that the game recognizes the horizontal win.
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Horizontal win should be detected.')

	def test_vertical_win(self):
		'''
		Test detection of a vertical win condition.

		@return None
		'''
		# Manually fill a vertical segment in the first column for the human.
		col = 0
		for row in range(self.connect_m):
			self.game.board[self.board_size - 1 - row][col] = self.game.human_symbol
		# Verify that the vertical win is detected.
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Vertical win should be detected.')

	def test_diagonal_win(self):
		'''
		Test detection of a diagonal win (top-left to bottom-right).

		@return None
		'''
		# Manually set up a diagonal win for the human.
		for i in range(self.connect_m):
			self.game.board[i][i] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Diagonal win should be detected.')

	def test_anti_diagonal_win(self):
		'''
		Test detection of an anti-diagonal win (top-right to bottom-left).

		@return None
		'''
		# Manually set up an anti-diagonal win for the human.
		for i in range(self.connect_m):
			self.game.board[i][self.board_size - 1 - i] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Anti-diagonal win should be detected.')

	def test_draw(self):
		'''
		Test that a full board with no wins is detected as a draw.

		@return None
		'''
		# Fill the board in an alternating pattern to avoid any wins.
		symbol_cycle = [self.game.human_symbol, self.game.computer_symbol]
		idx = 0
		for row in range(self.board_size):
			for col in range(self.board_size):
				self.game.board[row][col] = symbol_cycle[idx % 2]
				idx += 1
		self.assertTrue(self.game.checkDraw(), 'The game should be detected as a draw when board is full.')

	def test_alpha_beta_search(self):
		'''
		Test that the alpha-beta search returns a valid move.

		@return None
		'''
		# Simulate a scenario with a few moves already played.
		self.game.makeMove(0, self.game.human_symbol)
		self.game.makeMove(1, self.game.human_symbol)
		self.game.makeMove(2, self.game.computer_symbol)
		# Use the alpha-beta search to choose a move.
		move = self.game.alphaBetaSearch(depth=3)
		# Check that the move is one of the valid moves.
		self.assertIn(move, self.game.getValidMoves(self.game.board), 'Alpha-beta search should return a valid move.')

	def test_evaluate_board_state(self):
		'''
		Test that the evaluation function scores winning conditions correctly.

		@return None
		'''
		# Simulate a winning board for the computer.
		for col in range(self.connect_m):
			self.game.board[self.board_size - 1][col] = self.game.computer_symbol
		eval_score = self.game.evaluateBoardState(self.game.board)
		# The evaluation should be highly positive for a computer win.
		self.assertGreater(eval_score, 0, 'Evaluation should be positive for computer win.')

		# Reset the game and simulate a winning board for the human.
		self.game = ConnectMGame(self.board_size, self.connect_m, True)
		for col in range(self.connect_m):
			self.game.board[self.board_size - 1][col] = self.game.human_symbol
		eval_score = self.game.evaluateBoardState(self.game.board)
		# The evaluation should be highly negative for a human win.
		self.assertLess(eval_score, 0, 'Evaluation should be negative for human win.')

class TestMainCLI(unittest.TestCase):
	'''
	Unit tests for the CLI functionality in main.py.

	These tests simulate command-line invocations of main.py using subprocess
	and check that invalid inputs produce proper error messages and exit codes.
	'''

	def run_main(self, args):
		'''
		Helper method to run main.py with given command-line arguments.

		@param args: List of arguments (excluding the interpreter).
		@return: CompletedProcess object containing stdout, stderr, and return code.
		'''
		return subprocess.run([sys.executable, 'main.py'] + args,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	def test_missing_arguments(self):
		'''
		Test that running main.py without arguments produces a usage error.

		@return None
		'''
		result = self.run_main([])
		# Check that the process exits with a non-zero code.
		self.assertNotEqual(result.returncode, 0, 'Missing arguments should cause a non-zero exit.')
		# Check that the usage message is displayed.
		self.assertIn('Usage:', result.stdout, 'Usage message should be printed on missing arguments.')

	def test_invalid_board_size(self):
		'''
		Test that an invalid board size produces an error.

		@return None
		'''
		result = self.run_main(['2', '3', '1'])
		self.assertNotEqual(result.returncode, 0, 'Invalid board size should cause a non-zero exit.')
		self.assertIn('Board size N must be between 3 and 10.', result.stdout,
			'Error message for board size should be printed.')

	def test_invalid_connect_m(self):
		'''
		Test that an invalid connect M parameter produces an error.

		@return None
		'''
		result = self.run_main(['5', '6', '1'])
		self.assertNotEqual(result.returncode, 0, 'Invalid connect M should cause a non-zero exit.')
		self.assertIn('Parameter M must be higher than 1 and no higher than N.', result.stdout,
			'Error message for connect M should be printed.')

	def test_invalid_h_flag(self):
		'''
		Test that an invalid human/computer flag produces an error.

		@return None
		'''
		result = self.run_main(['5', '4', '2'])
		self.assertNotEqual(result.returncode, 0, 'Invalid H flag should cause a non-zero exit.')
		self.assertIn('Parameter H must be 0 or 1.', result.stdout,
			'Error message for H flag should be printed.')

# Run the test suite with increased verbosity if this script is executed directly.
if __name__ == '__main__':
	unittest.main(verbosity=2)
