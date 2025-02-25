#!/usr/bin/env python3
'''
Connect M Game Implementation.

This module contains a detailed implementation of the Connect M game logic using
adversarial search with alpha-beta pruning.

@author Jairun Diemert
@date 2025-02-24
@info CAP 4601 Project 1: Adversarial Search Spring 2025

'''

import copy  # Import the copy module to make deep copies of the game board when needed.

class ConnectMGame:
	'''
	Class representing the Connect M game logic.

	This class holds the game board and all game logic such as move validation,
	win/draw detection, and the adversarial search algorithm (alpha-beta pruning)
	to choose the best move for the computer.

	@param board_size: The size (number of rows and columns) of the square game board.
	@param connect_m: The number of disks that must be connected to win the game.
	@param human_first: A flag (True/False) indicating if the human moves first.
	'''

	def __init__(self, board_size, connect_m, human_first):
		'''
		Initializes the game with the board size, win condition, and first-move flag.

		@param board_size: Integer for the board dimensions (board_size x board_size).
		@param connect_m: Integer for the number of connected disks needed to win.
		@param human_first: Boolean indicating whether the human player starts.
		'''
		# Save the board size and the win condition for later use.
		self.board_size = board_size
		self.connect_m = connect_m
		# Save whether the human goes first.
		self.human_first = human_first
		# Define the symbols for the human and computer players.
		self.human_symbol = 'X'
		self.computer_symbol = 'O'
		# Initialize the board as a 2D list filled with spaces to represent empty cells.
		self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

	def displayBoard(self):
		'''
		Displays the current game board in a simple text format.

		It prints a border, then each row of the board with cell values.
		'''
		# Print the top border of the board.
		print('+' + '---+' * self.board_size)
		# Iterate rows of the board.
		for row in self.board:
			# Start building the row string with a left border.
			row_str = '|'
			# Loop through each cell in the row.
			for cell in row:
				# Add the cell value inside a box (with spaces around it).
				row_str += ' ' + cell + ' |'
			# Print the row.
			print(row_str)
			# Print a border after each row.
			print('+' + '---+' * self.board_size)

	def isValidMove(self, column):
		'''
		Checks if a move can be made in the given column.

		@param column: Integer index of the column to check.
		@return: True if the top cell in the column is empty, False if the column is full.
		'''
		# The move is valid if the top cell of the column is empty (a space).
		return self.board[0][column] == ' '

	def makeMove(self, column, symbol):
		'''
		Makes a move by dropping a disk into the specified column.

		@param column: Integer index of the column (0-indexed).
		@param symbol: Character representing the player's disk (X or O).
		@return: True if the disk was placed successfully, False if the column is full.
		'''
		# First, check if the move is valid (i.e., the column is not full).
		if not self.isValidMove(column):
			return False
		# Iterate over the rows starting from the bottom (last index) up to the top.
		# For example, if board_size = 5, the row indices will be: 4 -> 3 -> 2 -> 1 -> 0
		for row in range(self.board_size - 1, -1, -1):
			# Find the first empty cell in the column.
			if self.board[row][column] == ' ':
				# Place the disk (set the cell to the player's symbol).
				self.board[row][column] = symbol
				# Return True to indicate the move was successful.
				return True
		# If no empty cell is found, return False.
		return False

	def checkWin(self, symbol):
		'''
		Checks if the player with the given symbol has won the game.

		@param symbol: Character representing the player's disk.
		@return: True if the player has a winning set of connected disks, False otherwise.
		'''
		# Call the helper function checkWinState on the current board.
		return self.checkWinState(self.board, symbol)

	def checkWinState(self, board, symbol):
		'''
		Checks for a win condition on a given board for the specified symbol.

		@param board: 2D list representing the current board state.
		@param symbol: Character representing the player's disk.
		@return: True if a winning sequence is found, False otherwise.
		'''
		# Define the four directions to check for a winning sequence:
		#   (0, 1)  -> →  (horizontal right)
		#   (1, 0)  -> ↓  (vertical down)
		#   (1, 1)  -> ↘ (diagonal down-right)
		#   (1, -1) -> ↙ (diagonal down-left)
		directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
		# Loop over every cell in the board.
		for row in range(self.board_size):
			for col in range(self.board_size):
				# Only start checking if the cell contains the player's symbol.
				if board[row][col] == symbol:
					# For each direction, count how many same-symbol cells are connected.
					for d in directions:
						count = 1  # Start with the current cell.
						# Set the next cell position based on the direction.
						r = row + d[0]
						c = col + d[1]
						# Continue moving in the chosen direction while within board limits.
						while 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == symbol:
							count += 1  # Increase the count for each connected disk.
							# If the count reaches the required number, a win is detected.
							if count >= self.connect_m:
								return True
							# Move to the next cell in the same direction.
							r += d[0]
							c += d[1]
		# If no winning sequence is found, return False.
		return False

	def checkDraw(self):
		'''
		Checks if the game is a draw.

		A draw is defined as a board where no valid moves remain (i.e., the top row is full).

		@return: True if the game is a draw, False otherwise.
		'''
		# Loop through every column in the top row.
		for col in range(self.board_size):
			# If any column is still empty, then moves can still be made.
			if self.board[0][col] == ' ':
				return False
		# If no columns have empty spaces, the board is full and it's a draw.
		return True

	def evaluateBoardState(self, board):
		'''
		Provides a heuristic evaluation of the board state.

		This function assigns a high positive value if the computer wins, a high negative
		value if the human wins, and otherwise scores potential winning segments.

		@param board: 2D list representing the board state.
		@return: Integer score representing the board's heuristic value.
		'''
		# Check if the computer has a winning sequence.
		# Example: For connect_m = 4, if a row has: O O O O => winning sequence.
		if self.checkWinState(board, self.computer_symbol):
			return 1000000

		# Check if the human has a winning sequence.
		# Example: For connect_m = 4, if a row has: X X X X => winning sequence.
		if self.checkWinState(board, self.human_symbol):
			return -1000000

		# Start with a score of zero for non-terminal states.
		score = 0

		# ================================================
		# Evaluate horizontal segments (rows).
		# ================================================
		# Imagine a row on the board as:
		# [ ' ', 'X', 'O', 'X', ' ' ]
		# For connect_m = 3, we extract segments like:
		#   Segment 1: [ ' ', 'X', 'O' ]
		#   Segment 2: [ 'X', 'O', 'X' ]
		#   Segment 3: [ 'O', 'X', ' ' ]
		# Each segment is then evaluated to see how favorable it is.
		for row in board:
			for col in range(self.board_size - self.connect_m + 1):
				segment = row[col:col + self.connect_m]
				score += self.evaluateSegment(segment)

		# ================================================
		# Evaluate vertical segments (columns).
		# ================================================
		# Consider a column on the board:
		# [
		#   ' ',
		#   'O',
		#   'X',
		#   'X',
		#   'O'
		# ]
		# For connect_m = 3, we take segments like:
		#   Segment 1: [ ' ', 'O', 'X' ]
		#   Segment 2: [ 'O', 'X', 'X' ]
		#   Segment 3: [ 'X', 'X', 'O' ]
		# Each segment is then scored.
		for col in range(self.board_size):
			for row in range(self.board_size - self.connect_m + 1):
				segment = [board[r][col] for r in range(row, row + self.connect_m)]
				score += self.evaluateSegment(segment)

		# ================================================
		# Evaluate diagonal segments (top-left to bottom-right).
		# ================================================
		# Visualize a portion of the board:
		# [ A, B, C, D ]
		# [ E, F, G, H ]
		# [ I, J, K, L ]
		# [ M, N, O, P ]
		#
		# For connect_m = 3, a diagonal segment starting at cell A (row 0, col 0)
		# would be: [ A, F, K ]
		# Similarly, starting at cell B (row 0, col 1) yields: [ B, G, L ]
		# The code extracts all such diagonals.
		for row in range(self.board_size - self.connect_m + 1):
			for col in range(self.board_size - self.connect_m + 1):
				segment = [board[row + i][col + i] for i in range(self.connect_m)]
				score += self.evaluateSegment(segment)

		# ================================================
		# Evaluate anti-diagonal segments (top-right to bottom-left).
		# ================================================
		# Using the same board visualization as above:
		# [ A, B, C, D ]
		# [ E, F, G, H ]
		# [ I, J, K, L ]
		# [ M, N, O, P ]
		#
		# For connect_m = 3, an anti-diagonal segment starting at cell D (row 0, col 3)
		# would be: [ D, G, J ]
		# Similarly, starting at cell C (row 0, col 2) yields: [ C, F, I ]
		# The code extracts all such anti-diagonals.
		for row in range(self.board_size - self.connect_m + 1):
			for col in range(self.connect_m - 1, self.board_size):
				segment = [board[row + i][col - i] for i in range(self.connect_m)]
				score += self.evaluateSegment(segment)

		# Return the total heuristic score for the board.
		return score

	def evaluateSegment(self, segment):
		'''
		Evaluates a segment of cells for potential winning opportunities.

		If the segment contains both players' symbols, it has no potential.
		Otherwise, segments with only one player's disks are scored exponentially
		based on the count of disks.

		@param segment: List of cell values (characters).
		@return: Integer score for the segment.
		'''
		# If both players have disks in the segment, it is blocked.
		if segment.count(self.human_symbol) > 0 and segment.count(self.computer_symbol) > 0:
			return 0
		# If only the computer's disks are present, return a positive score.
		elif segment.count(self.computer_symbol) > 0:
			return 10* segment.count(self.computer_symbol)
		# If only the human's disks are present, return a negative score.
		elif segment.count(self.human_symbol) > 0:
			return -(10* segment.count(self.human_symbol))
		else:
			# If the segment is completely empty, it has no score.
			return 0

	def getValidMoves(self, board):
		'''
		Generates a list of valid column indices where a move can be made.

		@param board: 2D list representing the board state.
		@return: List of integer column indices that are valid moves.
		'''
		valid_moves = []
		# Loop over each column.
		for col in range(self.board_size):
			# If the top cell of the column is empty, then the move is valid.
			if board[0][col] == ' ':
				valid_moves.append(col)
		return valid_moves

	def applyMove(self, board, move, symbol):
		'''
		Applies a move on a given board and returns a new board state.

		@param board: 2D list representing the current board.
		@param move: Integer column index where the disk is to be dropped.
		@param symbol: Character representing the player's disk.
		@return: A new board state after applying the move.
		'''
		# Create a deep copy of the board to avoid modifying the original board.
		new_board = copy.deepcopy(board)
		# Iterate over the rows starting from the bottom (last index) up to the top.
		# For example, if board_size = 5, the row indices will be: 4 -> 3 -> 2 -> 1 -> 0
		for row in range(self.board_size - 1, -1, -1):
			# Find the first empty spot in the selected column.
			if new_board[row][move] == ' ':
				# Place the disk.
				new_board[row][move] = symbol
				# Once the disk is placed, exit the loop.
				break
		# Return the new board state with the move applied.
		return new_board

	def checkTerminal(self, board):
		'''
		Determines if the board state is terminal.

		A terminal state is reached if either player has won or if there are no more valid moves.

		@param board: 2D list representing the board state.
		@return: True if the state is terminal (win or draw), False otherwise.
		'''
		# Check if either player has achieved a win.
		if self.checkWinState(board, self.computer_symbol) or self.checkWinState(board, self.human_symbol):
			return True
		# Check if there are no valid moves remaining.
		if not self.getValidMoves(board):
			return True
		return False

	def alphaBetaSearch(self, depth):
		'''
		Uses the alpha-beta pruning algorithm to choose the best move for the computer.

		@param depth: Integer specifying how many moves ahead to search.
		@return: The column index of the best move.
		'''
		# Initialize best score to a very small number and best move to None.
		best_score = -float('inf')
		best_move = None
		# Set initial alpha and beta values.
		alpha = -float('inf')
		beta = float('inf')
		# Get the list of all valid moves from the current board state.
		valid_moves = self.getValidMoves(self.board)
		# Loop through each valid move.
		for move in valid_moves:
			# Create a new board state by applying the move.
			new_board = self.applyMove(self.board, move, self.computer_symbol)
			# Evaluate the board state using the minimizer function.
			score = self.minValue(new_board, alpha, beta, depth - 1)
			# If this move has a better score, update best_score and best_move.
			if score > best_score:
				best_score = score
				best_move = move
			# Update alpha value.
			alpha = max(alpha, best_score)
		# Return the column index of the best move found.
		return best_move

	def maxValue(self, board, alpha, beta, depth):
		'''
		The maximizer function in the alpha-beta pruning algorithm.

		@param board: 2D list representing the board state.
		@param alpha: The best already explored option along the path to the root for the maximizer.
		@param beta: The best already explored option along the path to the root for the minimizer.
		@param depth: Integer representing the remaining search depth.
		@return: The maximum heuristic score for the board state.
		'''
		# If we've reached the desired depth or a terminal state, evaluate the board.
		if depth == 0 or self.checkTerminal(board):
			return self.evaluateBoardState(board)
		# Start with the lowest possible value.
		value = -float('inf')
		# Loop through all valid moves.
		for move in self.getValidMoves(board):
			# Apply the move for the computer.
			new_board = self.applyMove(board, move, self.computer_symbol)
			# Recursively call minValue to evaluate the opponent's best response.
			value = max(value, self.minValue(new_board, alpha, beta, depth - 1))
			# If the current value is greater than or equal to beta, prune the branch.
			if value >= beta:
				return value
			# Update alpha value.
			alpha = max(alpha, value)
		return value

	def minValue(self, board, alpha, beta, depth):
		'''
		The minimizer function in the alpha-beta pruning algorithm.

		@param board: 2D list representing the board state.
		@param alpha: The best already explored option for the maximizer.
		@param beta: The best already explored option for the minimizer.
		@param depth: Integer representing the remaining search depth.
		@return: The minimum heuristic score for the board state.
		'''
		# If the depth is zero or the state is terminal, evaluate the board.
		if depth == 0 or self.checkTerminal(board):
			return self.evaluateBoardState(board)
		# Start with the highest possible value.
		value = float('inf')
		# Loop through all valid moves.
		for move in self.getValidMoves(board):
			# Apply the move for the human.
			new_board = self.applyMove(board, move, self.human_symbol)
			# Recursively call maxValue to evaluate the computer's best response.
			value = min(value, self.maxValue(new_board, alpha, beta, depth - 1))
			# If the value is less than or equal to alpha, prune the branch.
			if value <= alpha:
				return value
			# Update beta value.
			beta = min(beta, value)
		return value
