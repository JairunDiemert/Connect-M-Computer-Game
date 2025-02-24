#!/usr/bin/env python3
'''
Test Suite for Connect M Game.

This module contains unit tests for both the game logic in the ConnectMGame class
and the CLI functionality in main.py. In addition, it simulates multiple games of
computer vs. computer to record outcomes.

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
															stdout=subprocess.PIPE, stderr=subprocess.PIPE,
															universal_newlines=True)

		def test_missing_arguments(self):
				'''
				Test that running main.py without arguments produces a usage error.

				@return None
				'''
				result = self.run_main([])
				self.assertNotEqual(result.returncode, 0, 'Missing arguments should cause a non-zero exit.')
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

class TestComputerVsComputer(unittest.TestCase):
		'''
		Simulate games where the computer plays against itself.

		In this simulation, both players use the alpha-beta search algorithm.
		Since the original game logic is designed for human vs. computer, we temporarily
		swap the symbols for the second player to simulate a computer move. The outcomes
		(AI #1 wins, AI #2 wins, or draw) are recorded over multiple games.
		'''

		def simulate_computer_move(self, game, player, depth):
				'''
				Simulate a move for the specified player using alpha-beta search.

				For AI #1, use the game instance as is.
				For AI #2, swap the computer and human symbols temporarily to simulate the move.

				@param game: The current ConnectMGame instance.
				@param player: Integer (1 or 2) indicating the current player.
				@param depth: Search depth for the alpha-beta algorithm.
				@return: None
				'''
				if player == 1: # AI #1
						move = game.alphaBetaSearch(depth)
						if move is not None:
								game.makeMove(move, game.computer_symbol)
				else:  # # AI #2
						# Swap symbols so that alphaBetaSearch works for the other player.
						game.computer_symbol, game.human_symbol = game.human_symbol, game.computer_symbol
						move = game.alphaBetaSearch(depth)
						if move is not None:
								game.makeMove(move, game.computer_symbol)
						# Swap symbols back to original.
						game.computer_symbol, game.human_symbol = game.human_symbol, game.computer_symbol

		def simulate_game(self, depth1=4, depth2=4):
				'''
				Simulate a full game between two computer players with different search depths.

				@param depth1: Search depth for AI #1.
				@param depth2: Search depth for AI #2.
				@return: String representing the outcome.
				'''
				board_size = 5
				connect_m = 4
				# Initialize the game; by default, computer_symbol ('O') is first, human_symbol ('X') is second.
				game = ConnectMGame(board_size, connect_m, human_first=True)
				current_player = 1
				while True:
						# Check if the game has reached a terminal state.
						if game.checkWin(game.computer_symbol) or game.checkWin(game.human_symbol) or game.checkDraw():
								break
						# Simulate move for the current player with different depths.
						if current_player == 1:
								self.simulate_computer_move(game, current_player, depth1)
						else:
								self.simulate_computer_move(game, current_player, depth2)
						# Switch players: if current_player was 1, then 2; otherwise 1.
						current_player = 2 if current_player == 1 else 1

				if game.checkWin('O'):
						return 'AI #1 WINS'
				elif game.checkWin('X'):
						return 'AI #2 WINS'
				else:
						return 'draw'

		def test_computer_vs_computer(self):
				'''
				Simulate a series of computer vs. computer games and record the outcomes.

				@return None
				'''
				num_games = 10  # Number of games to simulate.
				outcomes = {'AI #1 WINS': 0, 'AI #2 WINS': 0, 'draw': 0}
				for _ in range(num_games):
						# For instance, AI #1 uses depth 4, and AI #2 uses depth 2.
						result = self.simulate_game(depth1=2, depth2=1)
						outcomes[result] += 1
				# Print the outcomes for analysis.
				print('Outcomes after {} games: {}'.format(num_games, outcomes))
				# Ensure that the total outcomes equal the number of games simulated.
				self.assertEqual(sum(outcomes.values()), num_games)

# Run the test suite with increased verbosity if this script is executed directly.
if __name__ == '__main__':
		unittest.main(verbosity=2)
