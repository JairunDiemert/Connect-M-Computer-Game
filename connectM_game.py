#!/usr/bin/env python3
'''
/**
 * Connect M Game Implementation.
 *
 * This module contains the implementation of the Connect M game logic using adversarial search with alpha-beta pruning.
 *
 * @author Jairun Diemert
 * @date 2025-02-24
 * @info CAP 4601 Project 1: Adversarial Search Spring 2025
 */
'''

import copy

class ConnectMGame:
	'''
	/**
	 * Class representing the Connect M game logic.
	 *
	 * This class encapsulates the game state and implements the adversarial search
	 * algorithm with alpha-beta pruning to determine the optimal move for the computer.
	 *
	 * @param board_size: integer representing the number of rows and columns of the board.
	 * @param connect_m: integer representing the number of contiguous disks required to win.
	 * @param human_first: boolean flag indicating if the human player moves first.
	 */
	'''

	def __init__(self, board_size, connect_m, human_first):
		'''
		/**
		 * Initializes the Connect M game.
		 *
		 * @param board_size: number of rows/columns.
		 * @param connect_m: number of contiguous disks required to win.
		 * @param human_first: boolean indicating if human moves first.
		 */
		'''
		self.board_size = board_size
		self.connect_m = connect_m
		self.human_first = human_first
		self.human_symbol = 'X'
		self.computer_symbol = 'O'
		self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

	def displayBoard(self):
		'''
		/**
		 * Displays the current board state in a text-based visualization.
		 */
		'''
		# Print the top border
		print(('+' + '---+' * self.board_size))
		for row in self.board:
			row_str = '|'
			for cell in row:
				row_str += ' ' + cell + ' |'
			print(row_str)
			print(('+' + '---+' * self.board_size))

	def isValidMove(self, column):
		'''
		/**
		 * Checks if a move in the specified column is valid.
		 *
		 * @param column: integer representing the column index.
		 *
		 * @return True if the move is valid, False otherwise.
		 */
		'''
		return self.board[0][column] == ' '

	def makeMove(self, column, symbol):
		'''
		/**
		 * Drops a disk into the specified column for the given player symbol.
		 *
		 * @param column: integer representing the column index (0-indexed).
		 * @param symbol: character representing the player's disk.
		 *
		 * @return True if the move was successful, False otherwise.
		 */
		'''
		if not self.isValidMove(column):
			return False
		# Place the disk in the lowest available row in the column
		for row in range(self.board_size - 1, -1, -1):
			if self.board[row][column] == ' ':
				self.board[row][column] = symbol
				return True
		return False

	def checkWin(self, symbol):
		'''
		/**
		 * Checks if the specified player has won the game.
		 *
		 * @param symbol: character representing the player's disk.
		 *
		 * @return True if the player has a winning sequence, False otherwise.
		 */
		'''
		return self.checkWinState(self.board, symbol)

	def checkWinState(self, board, symbol):
		'''
		/**
		 * Checks if the specified player has a winning sequence on a given board state.
		 *
		 * @param board: 2D list representing the board state.
		 * @param symbol: character representing the player's disk.
		 *
		 * @return True if there is a winning sequence, False otherwise.
		 */
		'''
		directions = [(0,1), (1,0), (1,1), (1,-1)]
		for row in range(self.board_size):
			for col in range(self.board_size):
				if board[row][col] == symbol:
					for d in directions:
						count = 1
						r = row + d[0]
						c = col + d[1]
						while 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == symbol:
							count += 1
							if count >= self.connect_m:
								return True
							r += d[0]
							c += d[1]
		return False

	def checkDraw(self):
		'''
		/**
		 * Checks if the game is a draw (i.e., no valid moves left).
		 *
		 * @return True if the game is a draw, False otherwise.
		 */
		'''
		# If no valid moves, it's a draw.
		for col in range(self.board_size):
			if self.board[0][col] == ' ':
				return False
		return True

	def evaluateBoardState(self, board):
		'''
		/**
		 * Evaluates the given board state and returns a heuristic score.
		 *
		 * @param board: 2D list representing the board state.
		 *
		 * @return integer heuristic score.
		 */
		'''
		if self.checkWinState(board, self.computer_symbol):
			return 1000000
		if self.checkWinState(board, self.human_symbol):
			return -1000000
		score = 0
		# Evaluate horizontal segments
		for row in board:
			for col in range(self.board_size - self.connect_m + 1):
				segment = row[col:col + self.connect_m]
				score += self.evaluateSegment(segment)
		# Evaluate vertical segments
		for col in range(self.board_size):
			for row in range(self.board_size - self.connect_m + 1):
				segment = [board[r][col] for r in range(row, row + self.connect_m)]
				score += self.evaluateSegment(segment)
		# Evaluate diagonal (top-left to bottom-right)
		for row in range(self.board_size - self.connect_m + 1):
			for col in range(self.board_size - self.connect_m + 1):
				segment = [board[row + i][col + i] for i in range(self.connect_m)]
				score += self.evaluateSegment(segment)
		# Evaluate diagonal (top-right to bottom-left)
		for row in range(self.board_size - self.connect_m + 1):
			for col in range(self.connect_m - 1, self.board_size):
				segment = [board[row + i][col - i] for i in range(self.connect_m)]
				score += self.evaluateSegment(segment)
		return score

	def evaluateSegment(self, segment):
		'''
		/**
		 * Evaluates a segment (list) of cells and returns a score based on potential for winning.
		 *
		 * @param segment: list of characters representing a line segment on the board.
		 *
		 * @return integer score for the segment.
		 */
		'''
		if segment.count(self.human_symbol) > 0 and segment.count(self.computer_symbol) > 0:
			return 0
		elif segment.count(self.computer_symbol) > 0:
			return 10 ** segment.count(self.computer_symbol)
		elif segment.count(self.human_symbol) > 0:
			return - (10 ** segment.count(self.human_symbol))
		else:
			return 0

	def getValidMoves(self, board):
		'''
		/**
		 * Returns a list of valid moves (column indices) for the given board state.
		 *
		 * @param board: 2D list representing the board state.
		 *
		 * @return list of valid column indices.
		 */
		'''
		valid_moves = []
		for col in range(self.board_size):
			if board[0][col] == ' ':
				valid_moves.append(col)
		return valid_moves

	def applyMove(self, board, move, symbol):
		'''
		/**
		 * Applies a move to a given board state and returns a new board state.
		 *
		 * @param board: 2D list representing the board state.
		 * @param move: integer representing the column index.
		 * @param symbol: character representing the player's disk.
		 *
		 * @return a new board state after the move is applied.
		 */
		'''
		new_board = copy.deepcopy(board)
		for row in range(self.board_size - 1, -1, -1):
			if new_board[row][move] == ' ':
				new_board[row][move] = symbol
				break
		return new_board

	def checkTerminal(self, board):
		'''
		/**
		 * Checks if the given board state is terminal (win or draw).
		 *
		 * @param board: 2D list representing the board state.
		 *
		 * @return True if the board state is terminal, False otherwise.
		 */
		'''
		if self.checkWinState(board, self.computer_symbol) or self.checkWinState(board, self.human_symbol):
			return True
		if not self.getValidMoves(board):
			return True
		return False

	def alphaBetaSearch(self, depth):
		'''
		/**
		 * Performs the alpha-beta search algorithm to determine the best move for the computer.
		 *
		 * @param depth: integer representing the search depth.
		 *
		 * @return the best column index to move.
		 */
		'''
		best_score = -float('inf')
		best_move = None
		alpha = -float('inf')
		beta = float('inf')
		valid_moves = self.getValidMoves(self.board)
		for move in valid_moves:
			new_board = self.applyMove(self.board, move, self.computer_symbol)
			score = self.minValue(new_board, alpha, beta, depth - 1)
			if score > best_score:
				best_score = score
				best_move = move
			alpha = max(alpha, best_score)
		return best_move

	def maxValue(self, board, alpha, beta, depth):
		'''
		/**
		 * Recursive function for the maximizer in the alpha-beta pruning algorithm.
		 *
		 * @param board: 2D list representing the board state.
		 * @param alpha: current alpha value.
		 * @param beta: current beta value.
		 * @param depth: integer representing the remaining search depth.
		 *
		 * @return the maximum heuristic score.
		 */
		'''
		if depth == 0 or self.checkTerminal(board):
			return self.evaluateBoardState(board)
		value = -float('inf')
		for move in self.getValidMoves(board):
			new_board = self.applyMove(board, move, self.computer_symbol)
			value = max(value, self.minValue(new_board, alpha, beta, depth - 1))
			if value >= beta:
				return value
			alpha = max(alpha, value)
		return value

	def minValue(self, board, alpha, beta, depth):
		'''
		/**
		 * Recursive function for the minimizer in the alpha-beta pruning algorithm.
		 *
		 * @param board: 2D list representing the board state.
		 * @param alpha: current alpha value.
		 * @param beta: current beta value.
		 * @param depth: integer representing the remaining search depth.
		 *
		 * @return the minimum heuristic score.
		 */
		'''
		if depth == 0 or self.checkTerminal(board):
			return self.evaluateBoardState(board)
		value = float('inf')
		for move in self.getValidMoves(board):
			new_board = self.applyMove(board, move, self.human_symbol)
			value = min(value, self.maxValue(new_board, alpha, beta, depth - 1))
			if value <= alpha:
				return value
			beta = min(beta, value)
		return value
