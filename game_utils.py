from enum import Enum
import numpy as np
from typing import Callable, Optional, Tuple

BOARD_COLS = 7
BOARD_ROWS = 6
BOARD_SHAPE = (BOARD_ROWS,BOARD_COLS)
INDEX_HIGHEST_ROW = BOARD_ROWS - 1
INDEX_LOWEST_ROW = 0

BoardPiece = np.int8  # The data type (dtype) of the board pieces
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

PlayerAction = np.int8  # The column to be played


class SavedState:
    pass


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """
    Returns an ndarray, shape BOARD_SHAPE and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    the_board = np.ndarray(BOARD_SHAPE,dtype=BoardPiece)
    the_board[:, :] = BoardPiece(0)
    return the_board


def pretty_print_board(board: np.ndarray) -> str:
    """
    Should return `board` converted to a human readable string representation,
    to be used when playing or printing diagnostics to the console (stdout). The piece in
    board[0, 0] of the array should appear in the lower-left in the printed string representation. Here's an example output, note that we use
    PLAYER1_Print to represent PLAYER1 and PLAYER2_Print to represent PLAYER2):
    |==============|
    |              |
    |              |
    |    X X       |
    |    O X X     |
    |  O X O O     |
    |  O O X X     |
    |==============|
    |0 1 2 3 4 5 6 |
    """
    pretty_painting = "|==============|\n"
    for i in range(BOARD_ROWS):
        pretty_painting += "|"
        for j in range(BOARD_COLS):
            if board[BOARD_ROWS-i-1,j] == NO_PLAYER:
                pretty_painting += NO_PLAYER_PRINT + ","
            elif board[BOARD_ROWS-i-1,j] == PLAYER1:
                pretty_painting += PLAYER1_PRINT + ","
            elif board[BOARD_ROWS-i-1,j] == PLAYER2:
                pretty_painting += PLAYER2_PRINT + ","
        pretty_painting += "|\n"

    pretty_painting += "|==============|\n"

    return pretty_painting


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    lines = pp_board.split('\n')
    board = np.zeros(BOARD_SHAPE, dtype=BoardPiece)

    for i in range(len(lines)):
        j_board = 0
        for j in range(len(lines[i])):
            if lines[i][j] == NO_PLAYER_PRINT:
                board[BOARD_ROWS-i-1, j_board] = NO_PLAYER
                j_board += 1
            elif lines[i][j] == PLAYER1_PRINT:
                board[BOARD_ROWS-i-1, j_board] = PLAYER1
                j_board += 1
            elif lines[i][j] == PLAYER2_PRINT:
                board[BOARD_ROWS-i-1, j_board] = PLAYER2
                j_board += 1

    return board


def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. Raises a ValueError
    if action is not a legal move. If it is a legal move, the modified version of the
    board is returned and the original board should remain unchanged (i.e., either set
    back or copied beforehand).
    """
    new_board = board
    for i in range(BOARD_ROWS):
        if board[i,action] == BoardPiece(1) or board[i,action] == BoardPiece(2):
            if i == INDEX_HIGHEST_ROW:
                raise ValueError()
            continue
        else:
            new_board[i, action] = BoardPiece(player)
            break
    return new_board


def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    """
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                return True

        # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

        # Check diagonals (from bottom-left to top-right)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

        # Check diagonals (from top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False


def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    if connected_four(board,player):
        return GameState.IS_WIN

    elif connected_four(board,player) is False and all(board[INDEX_HIGHEST_ROW,:]!=NO_PLAYER):
        return GameState.IS_DRAW

    else:
        return GameState.STILL_PLAYING
