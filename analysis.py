#!/usr/bin/env python3
"""
Analysis Script for Connect M Game with Comprehensive Visualizations.

Generates:
- Heatmaps for different board sizes (3x3 to 6x6)
- A bar chart showing total draws across board sizes
- Saves the output as 'combined_results.png'

Author: Jairun Diemert
Date: 2025-02-24
Info: CAP 4601 Project 1: Adversarial Search Spring 2025
"""

import matplotlib.pyplot as plt
import numpy as np
from connectM_game import ConnectMGame
import os

def simulate_computer_move(game, player, depth):
		if player == 1:
				move = game.alphaBetaSearch(depth)
				if move is not None:
						game.makeMove(move, game.computer_symbol)
		else:
				game.computer_symbol, game.human_symbol = game.human_symbol, game.computer_symbol
				move = game.alphaBetaSearch(depth)
				if move is not None:
						game.makeMove(move, game.computer_symbol)
				game.computer_symbol, game.human_symbol = game.human_symbol, game.computer_symbol

def simulate_game(board_size, connect_m, human_first, depth1, depth2, max_moves=None):
		if max_moves is None:
				max_moves = board_size * board_size

		game = ConnectMGame(board_size, connect_m, human_first)
		current_player = 1
		moves = 0
		while moves < max_moves:
				if game.checkWin(game.computer_symbol) or game.checkWin(game.human_symbol) or game.checkDraw():
						break
				if current_player == 1:
						simulate_computer_move(game, current_player, depth1)
				else:
						simulate_computer_move(game, current_player, depth2)
				current_player = 2 if current_player == 1 else 1
				moves += 1

		if game.checkWin('O'):
				return 'AI #1 WINS'
		elif game.checkWin('X'):
				return 'AI #2 WINS'
		else:
				return 'draw'

def run_parameter_sweep():
		board_sizes = [3, 4, 5, 6]
		depths_ai1 = [1, 2, 3, 4]
		depths_ai2 = [1, 2, 3, 4]
		first_move_flags = [True]

		results = {size: np.empty((4, 4), dtype=object) for size in board_sizes}
		num_games = 3

		for board_size in board_sizes:
				for depth1 in depths_ai1:
						for depth2 in depths_ai2:
								outcomes = {'AI #1 WINS': 0, 'AI #2 WINS': 0, 'draw': 0}
								for _ in range(num_games):
										outcome = simulate_game(board_size, board_size, True, depth1, depth2)
										outcomes[outcome] += 1
								results[board_size][depth1-1, depth2-1] = (outcomes['AI #1 WINS'], outcomes['AI #2 WINS'], outcomes['draw'])
								print(f'Board: {board_size}x{board_size}, Depths: {depth1} vs {depth2}, Outcomes: {outcomes}')

		generate_combined_visual(results)

def generate_combined_visual(results):
		fig, axes = plt.subplots(2, 3, figsize=(18, 10))
		boards = list(results.keys())

		for idx, board in enumerate(boards):
				row = idx // 3
				col = idx % 3
				outcomes = results[board]

				ai1_wins = np.array([[outcome[0] for outcome in row] for row in outcomes])
				ai2_wins = np.array([[outcome[1] for outcome in row] for row in outcomes])
				draws = np.array([[outcome[2] for outcome in row] for row in outcomes])

				combined_data = np.zeros_like(ai1_wins, dtype=int)
				combined_data[draws == 3] = 0  # Draws
				combined_data[ai1_wins > ai2_wins] = 1  # AI #1 wins
				combined_data[ai2_wins > ai1_wins] = -1  # AI #2 wins

				cmap = plt.colormaps.get_cmap('bwr').resampled(3)

				ax = axes[row, col]
				cax = ax.matshow(combined_data, cmap=cmap, vmin=-1, vmax=1)
				for (i, j), val in np.ndenumerate(combined_data):
						outcome = outcomes[i][j]
						if val == 0:
								ax.text(j, i, f'D:{outcome[2]}', ha='center', va='center', color='black')
						else:
								win_text = f'1:{outcome[0]}\n2:{outcome[1]}'
								ax.text(j, i, win_text, ha='center', va='center', color='black')

				ax.set_xticks(range(4))
				ax.set_yticks(range(4))
				ax.set_xticklabels([1, 2, 3, 4])
				ax.set_yticklabels([1, 2, 3, 4])
				ax.set_xlabel("AI #2 Depth")
				ax.set_ylabel("AI #1 Depth")
				ax.set_title(f'{board}x{board} Board')

		draws = [sum(outcome[2] for row in results[board] for outcome in row) for board in boards]
		ax = axes[1, 2]
		ax.bar([f'{b}x{b}' for b in boards], draws, color='gray')
		ax.set_title('Total Draws by Board Size')
		ax.set_xlabel('Board Size')
		ax.set_ylabel('Total Draws')

		axes[1, 1].axis('off')

		fig.suptitle('AI Alpha-Beta Search Depth Analysis Results', fontsize=16)
		plt.tight_layout(rect=[0, 0, 1, 0.95])

		output_dir = 'analysis_results'
		os.makedirs(output_dir, exist_ok=True)
		output_path = os.path.join(output_dir, 'combined_results.png')
		plt.savefig(output_path)
		plt.close()
		print(f"Combined analysis chart saved as '{output_path}'.")

if __name__ == '__main__':
		run_parameter_sweep()
