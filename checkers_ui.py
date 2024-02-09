from constants import *
from checkers_logic import CheckersLogic
import re
import sys
import os


class CheckersUI:
    """
    Manages the User Interface for a Checkers game. This includes displaying the game board,
    handling user inputs, and communicating game status messages to the player.
    """

    def __init__(self):
        """
        Initializes the CheckersUI.
        """
        self.game = CheckersLogic()

    def clear_screen(self):
        """
        Clears the console screen to make way for fresh output. Handles different
        operating systems.
        """
        # Check if the operating system is Windows
        if os.name == 'nt':
            os.system('cls')
        # For Unix, Linux, and macOS
        else:
            os.system('clear')

    def print_board(self):
        """
        Prints the current state of the game board to the console, including
        the positioning of pieces and board coordinates.
        """
        board_str = "\n      0 1 2 3 4 5 6 7\n   =====================\n"

        range_rows = range(len(self.game.board)-1, -1, -1)

        for row_index in range_rows:
            row = self.game.board[row_index]
            board_str += f"  {row_index}|| "
            for cell in row:

                if cell == GREEN_PIECE or cell == GREEN_QUEEN:
                    board_str += f"{GREEN}{cell} {RESET}"
                elif cell == ORANGE_PIECE or cell == ORANGE_QUEEN:
                    if cell == "0":
                        cell = "O"
                    else:
                        cell = "Q"
                    board_str += f"{ORANGE}{cell} {RESET}"
                else:
                    board_str += f"{cell} "
            board_str += "||\n"
        board_str += "   =====================\n"
        print(board_str)

    def validate_input(self, prompt: str) -> int:
        """
        Prompts the user for input and validates it to ensure it is a digit within the board's bounds.

        Args:
            prompt (str): The message displayed to the user asking for input.

        Returns:
            int: The validated input converted to an integer.
        """
        pattern = r"^[0-7]$"
        while True:
            user_input = input(prompt)
            if re.match(pattern, user_input):
                return int(user_input)
            else:
                self.print_board()

                self.print_error(
                    "Invalid input. Please enter a number between 0 and 7.")

    def print_error(self, text: str):
        """
        Displays an error message to the user.

        Args:
            text (str): The error message to be displayed.
        """

        print(f"{RED}{text}{RESET}")

    def ask_for_move(self) -> list[int]:
        """
        Asks the user to input the row and column numbers for their next move.

        Returns:
            list[int]: A list containing the target row and column as integers.
        """

        print("Move your piece: ")
        end_row = self.validate_input("Row: ")
        end_col = self.validate_input("Col: ")

        return [end_row, end_col]

    def ask_for_piece(self) -> list[int]:
        """
        Asks the user to select the piece they want to move by inputting its row and column numbers.

        Returns:
            list[int]: A list containing the row and column of the selected piece as integers.
        """
        print("Select your piece: ")
        correct_piece = False
        while not correct_piece:
            init_row = self.validate_input("Row: ")
            init_col = self.validate_input("Col: ")

            if (not self.game.check_valid_piece(init_row, init_col)):
                correct_piece = False
                self.print_board()
                self.print_error("Select a valid piece: ")
                continue
            correct_piece = True

        return [init_row, init_col]

    def move(self):
        """
        Manages the process of making a move in the game, including asking the user for input,
        validating the move, and updating the game state accordingly.
        """
        print(f"{ENUM_COLORS[self.game.current_player]}Player "
              f"{self.game.current_player}{RESET}")

        move_validated = False
        while (not move_validated):
            init_row, init_col = self.ask_for_piece()
            end_row, end_col = self.ask_for_move()
            move_validated, error = self.game.validate_move(
                init_row, init_col, end_row, end_col)

            if not move_validated:
                self.print_board()
                self.print_error(error)

        self.game.perform_move(init_row, init_col, end_row, end_col)

        if not self.game.winner:
            self.game.change_player()

    def play(self):
        """
        Starts and manages the gameplay loop, allowing players to take turns until the game ends.
        """

        self.game.init_game()
        self.clear_screen()
        self.game.current_player = PLAYER_GREEN
        print("\nThe game has just begun: good luck ;)\n")

        while not self.game.winner:
            self.print_board()
            self.move()
            # check for winner

        self.clear_screen()
        self.print_board()
        print(f"{ENUM_COLORS[self.game.current_player]}"
              f"The winner is player{self.game.winner} {RESET}")

        input("Enter any key to return to the menu")
        self.menu()

    def instructions(self):
        """
        Displays the game instructions to the user, including how to play, the rules, and the objective.
        """
        self.clear_screen()
        print("\033[1mCheckers Game Instructions\033[0m\n")  # Bold
        print("\033[1mObjective:\033[0m")  # Bold
        print("  The objective of Checkers is to eliminate all of the opponent's pieces from the board.\n")
        print("\033[1mPlayers:\033[0m")  # Bold
        print(f"  There are two players:")
        print(f"{GREEN}    Green")
        print(f"{RESET}{ORANGE}    Orange{RESET}\n")
        print("\033[1mMoving:\033[0m")  # Bold
        print("  - Normal pieces move forward diagonally to an adjacent empty square.")
        print("  - When a piece reaches the opposite side of the board, it becomes a Queen (Q), which can move both forward and backward diagonally.\n")
        print("\033[1mCapturing:\033[0m")  # Bold
        print("  - If an opponent's piece is adjacent and the square immediately beyond it is empty, you can jump over the opponent's piece and remove it from the board.")
        print("  - Multiple jumps are allowed if after the first jump, another capturing opportunity is available.")
        print("\033[1mWinning the Game:\033[0m")  # Bold
        print("  - You win by capturing all of the opponent's pieces or blocking them so they have no legal moves.\n")
        print("\033[1mGameplay:\033[0m")  # Bold
        print("  - Players take turns to move one piece at a time.")
        print("  - To move a piece, first select the piece by entering its row and column numbers, then enter the row and column numbers of the destination square.\n")
        print("\033[1mNote:\033[0m")  # Bold
        print("  - The board is an 8x8 grid, with rows and columns numbered from 0 to 7.")
        input("\nEnter any key to go back: ")

        self.menu()

    def menu(self):
        """
        Displays the main menu to the user, allowing them to start a new game, view instructions, or exit.
        """
        key_validated = False
        print("\n==========")
        print("|| MENU ||")
        print("==========\n")
        print("p: Start playing\n")
        print("i: Instructions\n")
        print("q: Close game\n")
        while not key_validated:
            key = input()
            key = key.lower()
            if key != "q" and key != "i" and key != "p":
                self.print_error("Please, enter a valid key: ")
            else:
                key_validated = True

        print(key)
        if key == "q":
            print("BYE BYE")
            sys.exit()
        if key == "i":
            self.instructions()
        if key == "p":
            self.play()
