#!/usr/bin/env python3
'''
/**
 * Main CLI for Connect M Game.
 *
 * This module is the command-line interface for the Connect M game. It handles user input,
 * validates parameters, initializes the game, and runs the main game loop.
 *
 * @author Jairun Diemert
 * @date 2025-02-24
 * @info CAP 4601 Project 1: Adversarial Search Spring 2025
 */
'''

import sys  # Import system module for accessing command-line arguments and exiting.
from connectM_game import ConnectMGame  # Import the game logic class.

def main():
	'''
	/**
	 * Main function to run the Connect M game.
	 *
	 * This function parses and validates command-line arguments, creates a game instance,
	 * and starts the main game loop where the human and computer take turns.
	 *
	 * @return None
	 */
	'''
	# Check if the number of command-line arguments is exactly 4:
	# [script name, board_size (N), connect_m (M), human_first flag (H)]
	if len(sys.argv) != 4:
		# If not, print usage information and exit with an error code.
		print('Usage: python3 main.py <N> <M> <H>')
		sys.exit(1)
	try:
		# Convert the command-line arguments to integers.
		board_size = int(sys.argv[1])
		connect_m = int(sys.argv[2])
		human_first_flag = int(sys.argv[3])
	except ValueError:
		# If conversion fails, print an error message and exit.
		print('All parameters must be integers.')
		sys.exit(1)
	# Validate that the board size is between 3 and 10.
	if board_size < 3 or board_size > 10:
		print('Board size N must be between 3 and 10.')
		sys.exit(1)
	# Validate that connect_m is at least 2 and does not exceed board_size.
	if connect_m < 2 or connect_m > board_size:
		print('Parameter M must be higher than 1 and no higher than N.')
		sys.exit(1)
	# Validate that the human/computer flag is either 0 or 1.
	if human_first_flag not in [0, 1]:
		print('Parameter H must be 0 or 1.')
		sys.exit(1)

	# Determine if the human should move first.
	human_first = True if human_first_flag == 1 else False
	# Create a new ConnectMGame instance with the specified parameters.
	game = ConnectMGame(board_size, connect_m, human_first)
	# Set the current player based on the human_first flag.
	current_player = 'human' if human_first else 'computer'

	# Begin the main game loop.
	while True:
		# Display the current game board.
		game.displayBoard()
		# Check if the human has won.
		if game.checkWin(game.human_symbol):
			print('Human wins!')
			break  # Exit the loop since the game is over.
		# Check if the computer has won.
		if game.checkWin(game.computer_symbol):
			print('Computer wins!')
			break  # Exit the loop since the game is over.
		# Check if the game is a draw (i.e., no valid moves remain).
		if game.checkDraw():
			print('The game is a draw.')
			break  # Exit the loop.

		# If it's the human player's turn:
		if current_player == 'human':
			try:
				# Prompt the human to enter a column number (1-indexed).
				user_input = input('Enter column (1-{}): '.format(board_size))
				# Convert the input to an integer and adjust for zero-indexing.
				column = int(user_input) - 1
			except ValueError:
				# If input conversion fails, notify the user and prompt again.
				print('Invalid input. Please enter a number.')
				continue
			# Check if the column number is within the valid range.
			if column < 0 or column >= board_size:
				print('Column out of range.')
				continue  # Prompt for input again.
			# Check if the chosen column has available space.
			if not game.isValidMove(column):
				print('Column is full. Choose another column.')
				continue  # Prompt for input again.
			# Make the move for the human player.
			game.makeMove(column, game.human_symbol)
			# Switch the turn to the computer.
			current_player = 'computer'
		else:
			# It is the computer's turn.
			print('Computer is thinking...')
			# Use the alpha-beta search algorithm to determine the best move.
			move = game.alphaBetaSearch(depth=4)
			# If no valid move is found, end the game.
			if move is None:
				print('No valid moves available. Game over.')
				break
			# Make the move for the computer.
			game.makeMove(move, game.computer_symbol)
			# Display the computer's move (convert from 0-indexed to 1-indexed).
			print('Computer places disk in column {}'.format(move + 1))
			# Switch the turn back to the human player.
			current_player = 'human'

# Run the main function only if this script is executed directly.
if __name__ == '__main__':
	main()
