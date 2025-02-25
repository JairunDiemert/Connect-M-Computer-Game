# **Connect M Game**

This is a Python implementation of the Connect M game using **adversarial search** with **alpha-beta pruning**. In this game, a human player competes against the computer by dropping disks into a grid. The objective is to connect **M** disks contiguously either horizontally, vertically, or diagonally.

---

## **Requirements**

- Python 3.x

---

## **Project Structure**

Here’s an overview of the project’s files and their purposes:

### **Essential Files (Core Functionality)**
These files are necessary to run and play the game:

- **`connectM_game.py`**
  Contains the core game logic, including the board setup, win condition checks, and implementation of the alpha-beta pruning algorithm for the computer’s decision-making.

- **`main.py`**
  Provides the **Command-Line Interface (CLI)** for starting and playing the game. It handles user input, initializes the game, and controls game flow.

- **`README.md`**
  This document, providing setup instructions, explanations of files, and guidelines on how to run and test the game.

- **`test.py`**
  A comprehensive test suite for verifying the integrity of the game logic and CLI functionality. It also runs automated simulations where two AIs compete, validating the fairness of the algorithm.

### **Additional Files (For Analysis and Reporting)**
These files are not necessary for basic gameplay but add extra analysis or documentation:

- **`analysis.py`**
  Runs in-depth simulations of AI vs. AI games across different board sizes and search depths. It generates visualizations (heatmaps and draw analysis) to analyze the effectiveness of the adversarial algorithm.

- **`combined_results_corrected.png`**
  A visualization produced by `analysis.py`, summarizing the results of AI simulations across different board configurations.

- **`REPORT.md`**
  The main project report detailing the design, implementation, and analysis outcomes of the Connect M game project.

- **`REPORT.pdf`**
  A PDF version of the report, formatted for easier sharing and reading.

- **`REPORT.html`**
  A HTML version of the report, used for in-browser previews.

---

## **How to Run the Game**

To start a game, open a terminal, navigate to the project directory, and run:

```bash
python3 main.py <N> <M> <H>
```

Where:
- `<N>` → The board size (number of rows and columns, between **3** and **10**).
- `<M>` → The number of contiguous disks required to win (must be between **2** and **N**).
- `<H>` → Flag for who moves first: `1` for the **human player** and `0` for the **computer**.

### **Example:**
Start a **5x5** game where **4** disks are needed to win and the human goes first:

```bash
python3 main.py 5 4 1
```

---

## **Configurable Parameters**

- **Board Size (N):**
  Sets the dimensions of the grid. Larger grids increase gameplay complexity.

- **Connect M (M):**
  Defines how many consecutive disks are required to win (horizontally, vertically, or diagonally).

- **First Move Flag (H):**
  Determines who makes the first move:
  - `1`: Human moves first
  - `0`: Computer moves first

- **Search Depth:**
  In `main.py`, the search depth for alpha-beta pruning is currently hardcoded to **4**. You can adjust this for better performance:
  - Higher depth → Stronger computer player (slower move selection)
  - Lower depth → Faster gameplay (potentially weaker AI)

  During testing 4 was chosen as a good balance between speed and performance.

---

## **Testing the Game**

A comprehensive test suite (`test.py`) verifies:
- **Game Logic:** Validates move legality, win/draw detection, heuristic evaluation, and alpha-beta pruning.
- **Command-Line Interface:** Tests error handling for invalid inputs.
- **AI Simulations:** Runs automated computer-vs.-computer matches to analyze the likelihood of draws or wins under different conditions.

### **Run Tests:**
Execute the following command:

```bash
python3 test.py
```

---

## **AI Analysis (Optional)**

Use `analysis.py` to run AI-vs.-AI simulations across various board sizes and depths. This script helps analyze:
- The relationship between board size and AI performance
- How search depth affects outcomes (wins, losses, draws)

The script generates a visualization (`combined_results_corrected.png`) summarizing the results.

### **Run Analysis:**
```bash
python3 analysis.py
```

---

Enjoy playing and analyzing the **Connect M Game**! 🚀