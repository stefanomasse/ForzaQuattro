from game_utils import *


def test_board_size():
    the_board = initialize_game_state()
    assert the_board.shape == BOARD_SHAPE


def test_empty_board():
    the_board = initialize_game_state()
    assert np.min(np.abs(the_board)) == 0


def test_connected_four_line():
    the_board = initialize_game_state()
    new_board = apply_player_action(the_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    assert connected_four(new_board,PLAYER1) is True
    assert check_end_state(new_board, PLAYER1) == GameState.IS_WIN


def test_connected_four_column():
    the_board = initialize_game_state()
    new_board = apply_player_action(the_board, 1, PLAYER1)
    new_board = apply_player_action(new_board, 2, PLAYER1)
    new_board = apply_player_action(new_board, 3, PLAYER1)
    new_board = apply_player_action(new_board, 4, PLAYER1)
    assert connected_four(new_board,PLAYER1) is True
    assert check_end_state(new_board, PLAYER1) == GameState.IS_WIN


def test_connected_four_diagonal():
    the_board = initialize_game_state()
    new_board = apply_player_action(the_board, 1, PLAYER1)
    new_board = apply_player_action(new_board, 2, PLAYER2)
    new_board = apply_player_action(new_board, 3, PLAYER1)
    new_board = apply_player_action(new_board, 4, PLAYER2)
    new_board = apply_player_action(the_board, 1, PLAYER2)
    new_board = apply_player_action(new_board, 2, PLAYER1)
    new_board = apply_player_action(new_board, 3, PLAYER2)
    new_board = apply_player_action(new_board, 1, PLAYER1)
    new_board = apply_player_action(the_board, 2, PLAYER2)
    new_board = apply_player_action(new_board, 1, PLAYER2)
    assert connected_four(new_board,PLAYER2) is True
    assert check_end_state(new_board, PLAYER2) == GameState.IS_WIN


def test_connected_four_false():
    the_board = initialize_game_state()
    new_board = apply_player_action(the_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    assert connected_four(new_board,PLAYER1) is False
    assert check_end_state(new_board,PLAYER1) == GameState.STILL_PLAYING


def test_connected_four_loser():
    the_board = initialize_game_state()
    new_board = apply_player_action(the_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    new_board = apply_player_action(new_board, 5, PLAYER1)
    assert connected_four(new_board,PLAYER2) is False
    assert check_end_state(new_board,PLAYER1) == GameState.IS_WIN


test_board_size()
test_empty_board()
test_connected_four_line()
test_connected_four_column()
test_connected_four_diagonal()
test_connected_four_false()
test_connected_four_loser()
print('passed')
