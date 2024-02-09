from constants import *


class CheckersLogic:
    """
    Manages the state and rules of a Checkers game, including tracking the game board, the current player,
    and handling moves and captures.
    """

    def __init__(self):
        """Initializes a new game of Checkers, setting up the board and starting conditions."""

        self.init_game()

    def init_game(self):
        """Sets up the game board with pieces in their starting positions and resets game state."""
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        for row_index in range(8):
            if row_index % 2 == 0:
                col_begin = 1
            else:
                col_begin = 0

            if row_index < 3:
                piece = GREEN_PIECE
            elif row_index > 4:
                piece = ORANGE_PIECE
            else:
                continue

            for col_index in range(col_begin, 8, 2):
                self.board[row_index][col_index] = piece

        self.green_pieces = 12
        self.orange_pieces = 12
        self.eaten_pieces = []
        self.current_player = PLAYER_GREEN
        self.winner = None
        self.memo = set([])

    def change_player(self):
        """Switches the current player to the other player."""
        self.current_player = PLAYER_GREEN if self.current_player == PLAYER_ORANGE else PLAYER_ORANGE

    def get_piece(self, row, col):
        """
        Returns the piece at the specified board position.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.

        Returns:
            str: The piece at the specified position.
        """
        return self.board[row][col]

    def check_valid_piece(self, init_row: int, init_col: int) -> bool:
        """
        Determines if the selected piece belongs to the current player and is a valid choice for movement.

        Args:
            init_row (int): The row index of the selected piece.
            init_col (int): The column index of the selected piece.

        Returns:
            bool: True if the piece is valid for the current player, False otherwise.
        """
        piece = self.get_piece(init_row, init_col)

        if (piece != ENUM_NORMAL[self.current_player] and piece != ENUM_PROMOTED[self.current_player]):
            return False
        return True

    def eat_pieces(self):
        """
        Removes captured pieces from the board and updates the count of pieces for each player.
        """

        counter = 0
        for piece in self.eaten_pieces:
            self.board[piece[0]][piece[1]] = EMPTY
            counter += 1

        if self.current_player == PLAYER_GREEN:
            self.orange_pieces -= counter
        else:
            self.green_pieces -= counter

        self.eaten_pieces = []

    def perform_move(self, init_row: int, init_col: int, end_row: int, end_col: int):
        """
        Performs the specified move, including capturing and piece promotion, and checks for game end.

        Args:
            init_row (int): The starting row of the move.
            init_col (int): The starting column of the move.
            end_row (int): The ending row of the move.
            end_col (int): The ending column of the move.

        Returns:
            bool: True if the move is performed successfully, False otherwise.
        """
        self.board[end_row][end_col] = self.board[init_row][init_col]

        if init_row != end_row or init_col != end_col:
            self.board[init_row][init_col] = EMPTY

        if len(self.eaten_pieces) > 0:
            self.eat_pieces()

        self.check_piece_promotion_and_promote(end_row, end_col)

        self.check_end()

        return True

    def check_piece_promotion_and_promote(self, end_row: int, end_col: int):
        """
        Promotes a piece to a Queen if it reaches the opposite side of the board.

        Args:
            end_row (int): The row index where the piece ends up.
            end_col (int): The column index where the piece ends up.
        """
        if self.current_player == PLAYER_GREEN and end_row == len(self.board)-1:
            self.board[end_row][end_col] = GREEN_QUEEN

        if self.current_player == PLAYER_ORANGE and end_row == 0:
            self.board[end_row][end_col] = ORANGE_QUEEN

    def check_basic_move(self, end_row: int, end_col: int) -> bool:
        """
        Checks if a basic move to an empty square is valid.

        Args:
            end_row (int): The row index of the destination square.
            end_col (int): The column index of the destination square.

        Returns:
            bool: True if the destination square is empty, False otherwise.
        """
        if self.get_piece(end_row, end_col) != EMPTY:
            return True
        return False

    def check_opposite(self, player: str, piece_two: str):
        """
        Determines if the specified piece belongs to the opponent.

        Args:
            player (str): The current player making the move.
            piece_two (str): The piece to check against.

        Returns:
            bool: True if the piece belongs to the opponent, False otherwise.
        """
        if piece_two in OPOSITES[player]:
            return True
        return False

    # TODO: We could include loops to make the code more concise. I would discussed it with my team in a real life scenario
    def check_longer_move(self, piece: str, init_row: int, init_col: int, end_row: int, end_col: int, eaten) -> bool:
        """
        Recursively checks for valid multi-capture moves and updates eaten pieces if successful.

        Args:
            piece (str): The piece making the move.
            init_row (int): The starting row index.
            init_col (int): The starting column index.
            end_row (int): The target row index.
            end_col (int): The target column index.
            eaten (list): The list of captured pieces' positions so far.

        Returns:
            bool: True if a valid capturing move to the target position exists, False otherwise.
        """

        # MEMO
        if (init_row, init_col) in self.memo:
            return
        self.memo.add((init_row, init_col))

        # BASE CASE
        if (init_row == end_row and init_col == end_col):
            self.eaten_pieces = eaten
            return True
        top_right, top_left, bottom_right, bottom_left = False, False, False, False

        # top-right top-left

        if (piece == GREEN_PIECE or piece == GREEN_QUEEN or piece == ORANGE_QUEEN):
            if init_row <= len(self.board)-3:
                # top_right
                if init_col >= 2 and self.check_opposite(self.current_player, self.board[init_row + 1][init_col-1]):
                    eaten_top_right = eaten + [(init_row + 1, init_col-1)]
                    top_right = self.check_longer_move(
                        piece, init_row + 2, init_col - 2, end_row, end_col, eaten_top_right)

                # top_left
                if init_col <= len(self.board)-3 and self.check_opposite(self.current_player, self.board[init_row + 1][init_col+1]):
                    eaten_top_left = eaten + [(init_row + 1, init_col+1)]
                    top_left = self.check_longer_move(
                        piece, init_row + 2, init_col + 2, end_row, end_col, eaten_top_left)

        # bottom-right and bottom-left
        if (piece == ORANGE_PIECE or piece == GREEN_QUEEN or piece == ORANGE_QUEEN):
            if init_row >= 2:
                # bottom_right
                if init_col <= len(self.board)-3 and self.check_opposite(self.current_player, self.board[init_row - 1][init_col+1]):
                    eaten_bottom_right = eaten + [(init_row - 1, init_col+1)]
                    bottom_right = self.check_longer_move(
                        piece, init_row - 2, init_col + 2, end_row, end_col, eaten_bottom_right)
                # bottom_left
                if init_col >= 2 and self.check_opposite(self.current_player, self.board[init_row - 1][init_col-1]):
                    eaten_bottom_left = eaten + [(init_row-1, init_col-1)]
                    bottom_left = self.check_longer_move(
                        piece, init_row - 2, init_col - 2, end_row, end_col, eaten_bottom_left)

        return top_right or top_left or bottom_right or bottom_left

    def check_wrong_direction(self, init_row: int, init_col: int, end_row: int) -> bool:
        """
        Checks if a move is in the wrong direction for the type of piece being moved.

        Args:
            init_row (int): The starting row index of the move.
            init_col (int): The starting column index of the move.
            end_row (int): The target row index of the move.

        Returns:
            bool: True if the move is in the wrong direction, False otherwise.
        """
        difference = end_row - init_row
        piece = self.get_piece(init_row, init_col)
        if piece == GREEN_PIECE and difference <= 0:
            return True

        if piece == ORANGE_PIECE and difference >= 0:
            return True

        return False

    def check_same_move(self, init_row: int, init_col: int, end_row: int, end_col: int) -> bool:
        """
        Determines if the start and end positions of a move are the same.

        Args:
            init_row (int): The starting row index of the move.
            init_col (int): The starting column index of the move.
            end_row (int): The target row index of the move.
            end_col (int): The target column index of the move.

        Returns:
            bool: True if the start and end positions are the same, False otherwise.
        """
        if (init_row == end_row and init_col == end_col):
            return True
        return False

    def validate_move(self, init_row: int, init_col: int, end_row: int, end_col: int) -> [bool, str]:
        """
        Validates the proposed move, checking for legality and adherence to game rules.

        Args:
            init_row (int): The starting row index of the move.
            init_col (int): The starting column index of the move.
            end_row (int): The target row index of the move.
            end_col (int): The target column index of the move.

        Returns:
            (bool, str): A tuple containing a boolean indicating if the move is valid and a message explaining why if not.
        """
        # if move is the same is not allowed
        if self.check_same_move(init_row, init_col, end_row, end_col):
            return False, "You have to move the piece"

        # check if normal piece is moving backwords
        if self.check_wrong_direction(init_row, init_col, end_row):
            return False, "You have to move forward"

        # check 1 unit diagonall movement
        if (abs(end_row - init_row) == 1 and abs(init_col - end_col) == 1):
            if self.check_basic_move(end_row, end_col):
                return False, "You can not move there, there is already a piece"
        else:
            # check movements of more than 1 unit
            self.memo = set([])
            if not self.check_longer_move(self.get_piece(init_row, init_col), init_row, init_col, end_row, end_col, []):
                return False, "That move is not allowed"

        return True, ""

    def check_end(self) -> bool:
        """
        Checks if the game has ended by one player losing all pieces.
        Updates the winner attribute if the game has ended.
        """
        if self.green_pieces == 0:
            self.winner = PLAYER_ORANGE

        if self.orange_pieces == 0:
            self.winner = PLAYER_GREEN
