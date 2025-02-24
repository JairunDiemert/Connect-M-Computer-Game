#!/usr/bin/env python3
'''
/**
 * Comprehensive Test Suite for Connect M Game.
 *
 * This module contains unit tests for the Connect M game implementation.
 * It covers both the game logic in the ConnectMGame class as well as the CLI
 * functionality in the main module via subprocess calls.
 *
 * @author Jairun Diemert
 * @date 2025-02-24
 * @info CAP 4601 Project 1: Adversarial Search Spring 2025
 */
'''

import unittest
import subprocess
import sys
from connectM_game import ConnectMGame

class TestConnectMGame(unittest.TestCase):
	'''
	/**
	 * Unit tests for the ConnectMGame class.
	 */
	'''

	def setUp(self):
		'''
		/**
		 * Setup for the test cases. Initializes a ConnectMGame instance.
		 */
		'''
		self.board_size = 5
		self.connect_m = 4
		self.game = ConnectMGame(self.board_size, self.connect_m, True)

	def test_is_valid_move(self):
		'''
		/**
		 * Tests that valid moves are correctly identified and invalid moves are rejected.
		 *
		 * @return None
		 */
		'''
		# Initially, all columns should be valid.
		for col in range(self.board_size):
			self.assertTrue(self.game.isValidMove(col), f'Column {col} should be valid on an empty board.')

		# Fill a column and test validity.
		col_to_fill = 2
		for _ in range(self.board_size):
			move_made = self.game.makeMove(col_to_fill, self.game.human_symbol)
			self.assertTrue(move_made, 'Move should be successful.')
		self.assertFalse(self.game.isValidMove(col_to_fill), 'Column should be full and invalid for a move.')

	def test_make_move(self):
		'''
		/**
		 * Tests that a move is correctly made on the board.
		 *
		 * @return None
		 */
		'''
		col = 1
		self.assertTrue(self.game.makeMove(col, self.game.human_symbol), 'Move should be successful.')
		# The disk should be placed at the bottom of the column.
		self.assertEqual(self.game.board[self.board_size - 1][col], self.game.human_symbol,
			'The disk should be placed at the bottom row.')

	def test_horizontal_win(self):
		'''
		/**
		 * Tests detection of a horizontal win condition.
		 *
		 * @return None
		 */
		'''
		# Manually create a horizontal win for human.
		row = self.board_size - 1
		for col in range(self.connect_m):
			self.game.board[row][col] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Horizontal win should be detected.')

	def test_vertical_win(self):
		'''
		/**
		 * Tests detection of a vertical win condition.
		 *
		 * @return None
		 */
		'''
		col = 0
		for row in range(self.connect_m):
			self.game.board[self.board_size - 1 - row][col] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Vertical win should be detected.')

	def test_diagonal_win(self):
		'''
		/**
		 * Tests detection of a diagonal win condition (top-left to bottom-right).
		 *
		 * @return None
		 */
		'''
		# Set up a diagonal win for human.
		for i in range(self.connect_m):
			self.game.board[i][i] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Diagonal win should be detected.')

	def test_anti_diagonal_win(self):
		'''
		/**
		 * Tests detection of an anti-diagonal win condition (top-right to bottom-left).
		 *
		 * @return None
		 */
		'''
		for i in range(self.connect_m):
			self.game.board[i][self.board_size - 1 - i] = self.game.human_symbol
		self.assertTrue(self.game.checkWin(self.game.human_symbol), 'Anti-diagonal win should be detected.')

	def test_draw(self):
		'''
		/**
		 * Tests that a draw is detected when no valid moves are available.
		 *
		 * @return None
		 */
		'''
		# Fill the board without creating a win. Alternate moves between human and computer.
		symbol_cycle = [self.game.human_symbol, self.game.computer_symbol]
		idx = 0
		for row in range(self.board_size):
			for col in range(self.board_size):
				self.game.board[row][col] = symbol_cycle[idx % 2]
				idx += 1
		self.assertTrue(self.game.checkDraw(), 'The game should be detected as a draw when board is full.')

	def test_alpha_beta_search(self):
		'''
		/**
		 * Tests that the alpha-beta search returns a valid move.
		 *
		 * @return None
		 */
		'''
		# Set up a board with a few moves.
		# Let human make a couple of moves.
		self.game.makeMove(0, self.game.human_symbol)
		self.game.makeMove(1, self.game.human_symbol)
		# Let computer make a move.
		self.game.makeMove(2, self.game.computer_symbol)
		move = self.game.alphaBetaSearch(depth=3)
		self.assertIn(move, self.game.getValidMoves(self.game.board), 'Alpha-beta search should return a valid move.')

	def test_evaluate_board_state(self):
		'''
		/**
		 * Tests that the evaluation function returns high positive for computer win and high negative for human win.
		 *
		 * @return None
		 */
		'''
		# Test for computer win.
		for col in range(self.connect_m):
			self.game.board[self.board_size - 1][col] = self.game.computer_symbol
		eval_score = self.game.evaluateBoardState(self.game.board)
		self.assertGreater(eval_score, 0, 'Evaluation should be positive for computer win.')

		# Reset board and test for human win.
		self.game = ConnectMGame(self.board_size, self.connect_m, True)
		for col in range(self.connect_m):
			self.game.board[self.board_size - 1][col] = self.game.human_symbol
		eval_score = self.game.evaluateBoardState(self.game.board)
		self.assertLess(eval_score, 0, 'Evaluation should be negative for human win.')

class TestMainCLI(unittest.TestCase):
	'''
	/**
	 * Tests for the CLI functionality in the main module.
	 * These tests use subprocess to simulate command-line invocations and
	 * verify that error conditions are properly handled.
	 */
	'''

	def run_main(self, args):
		'''
		/**
		 * Helper method to run main.py with specified arguments.
		 *
		 * @param args: list of command-line arguments (excluding the python interpreter).
		 * @return: CompletedProcess instance from subprocess.run.
		 */
		'''
		return subprocess.run([sys.executable, 'main.py'] + args,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	def test_missing_arguments(self):
		'''
		/**
		 * Tests that running main.py with missing arguments results in a usage error.
		 *
		 * @return None
		 */
		'''
		result = self.run_main([])
		self.assertNotEqual(result.returncode, 0, 'Missing arguments should cause a non-zero exit.')
		self.assertIn('Usage:', result.stdout, 'Usage message should be printed on missing arguments.')

	def test_invalid_board_size(self):
		'''
		/**
		 * Tests that providing an invalid board size causes an error.
		 *
		 * @return None
		 */
		'''
		result = self.run_main(['2', '3', '1'])
		self.assertNotEqual(result.returncode, 0, 'Invalid board size should cause a non-zero exit.')
		self.assertIn('Board size N must be between 3 and 10.', result.stdout,
			'Error message for board size should be printed.')

	def test_invalid_connect_m(self):
		'''
		/**
		 * Tests that providing an invalid connect M parameter causes an error.
		 *
		 * @return None
		 */
		'''
		result = self.run_main(['5', '6', '1'])
		self.assertNotEqual(result.returncode, 0, 'Invalid connect M should cause a non-zero exit.')
		self.assertIn('Parameter M must be higher than 1 and no higher than N.', result.stdout,
			'Error message for connect M should be printed.')

	def test_invalid_h_flag(self):
		'''
		/**
		 * Tests that providing an invalid human/computer flag causes an error.
		 *
		 * @return None
		 */
		'''
		result = self.run_main(['5', '4', '2'])
		self.assertNotEqual(result.returncode, 0, 'Invalid H flag should cause a non-zero exit.')
		self.assertIn('Parameter H must be 0 or 1.', result.stdout,
			'Error message for H flag should be printed.')

if __name__ == '__main__':
	unittest.main(verbosity=2)
