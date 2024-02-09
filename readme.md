
# NOTE:

The implementation of the full game of checkers has taken me about 7 hours of work. I have tried to code everything as I would do it in a normal working day, following best practices.

The most important part is the movement validation implementation (validate_move) (line 262 of checkers_logic.py), which is the same problem as the one presented in the interview. For this, I have also recursively checked for positions in which a player eats multiple pieces.

All the logic has been written by me, I have used chatgpt to write comments, docstrings, and the readme.

# Checkers Game Project

The Checkers game project is a simple, console-based implementation of the classic board game. It is structured into four main files, each serving a distinct role in the application:

## File Structure

1. **`constants.py`**: Defines all the constant values used throughout the project. This includes ANSI color codes for terminal output, piece type identifiers, player numbers, and mappings for piece types and colors.

2. **`checkers_logic.py`**: Contains the `CheckersLogic` class, which encapsulates the game logic. This class manages the game state, including the board configuration, the current player, and the logic for making moves, capturing pieces, and checking for game end conditions.

3. **`checkers_ui.py`**: Houses the `CheckersUI` class responsible for the user interface of the game. This class handles displaying the game board, interpreting user inputs, and communicating game status messages to the player.

4. **`main.py`**: Serves as the entry point for the application. It creates an instance of the `CheckersUI` class and starts the game by calling the appropriate method.

## How to Run

To start the game:

```bash
python main.py
