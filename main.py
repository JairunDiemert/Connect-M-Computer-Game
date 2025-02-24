#!/usr/bin/env python3
'''
/**
 * Main CLI for Connect M Game.
 *
 * This module contains the command-line interface for the Connect M game, handling user input and output.
 *
 * @author Jairun Diemert
 * @date 2025-02-24
 * @info CAP 4601 Project 1: Adversarial Search Spring 2025
 */
'''

import sys
from connectM_game import ConnectMGame

def main():
	'''
	/**
	 * Main function to run the Connect M game.
	 */
	'''
	# Check for proper number of arguments
	if len(sys.argv) != 4:
		print('Usage: python3 main.py <N> <M> <H>')
		sys.exit(1)
	try:
		board_size = int(sys.argv[1])
		connect_m = int(sys.argv[2])
		human_first_flag = int(sys.argv[3])
	except ValueError:
		print('All parameters must be integers.')
		sys.exit(1)
	# Validate parameters
	if board_size < 3 or board_size > 10:
		print('Board size N must be between 3 and 10.')
		sys.exit(1)
	if connect_m < 2 or connect_m > board_size:
		print('Parameter M must be higher than 1 and no higher than N.')
		sys.exit(1)
	if human_first_flag not in [0, 1]:
		print('Parameter H must be 0 or 1.')
		sys.exit(1)

	human_first = True if human_first_flag == 1 else False
	game = ConnectMGame(board_size, connect_m, human_first)
	current_player = 'human' if human_first else 'computer'

	# Main game loop
	while True:
		game.displayBoard()
		# Check for win or draw
		if game.checkWin(game.human_symbol):
			print('Human wins!')
			break
		if game.checkWin(game.computer_symbol):
			print('Computer wins!')
			break
		if game.checkDraw():
			print('The game is a draw.')
			break

		if current_player == 'human':
			# Human move
			try:
				user_input = input('Enter column (1-{}): '.format(board_size))
				column = int(user_input) - 1
			except ValueError:
				print('Invalid input. Please enter a number.')
				continue
			if column < 0 or column >= board_size:
				print('Column out of range.')
				continue
			if not game.isValidMove(column):
				print('Column is full. Choose another column.')
				continue
			game.makeMove(column, game.human_symbol)
			current_player = 'computer'
		else:
			# Computer move using alpha-beta search
			print('Computer is thinking...')
			move = game.alphaBetaSearch(depth=4)
			if move is None:
				print('No valid moves available. Game over.')
				break
			game.makeMove(move, game.computer_symbol)
			print('Computer places disk in column {}'.format(move + 1))
			current_player = 'human'

if __name__ == '__main__':
	main()
