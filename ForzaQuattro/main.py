from game_utils import *
from typing import Callable
from agents.agent_human_user import user_move

the_board = initialize_game_state()
print(the_board)
pretty_board = pretty_print_board(the_board)
print(pretty_board)
the_board = string_to_board(pretty_board)
print(the_board)
new_board = apply_player_action(the_board,5,PLAYER1)
the_board = new_board
new_board = apply_player_action(the_board,5,PLAYER1)
the_board = new_board
new_board = apply_player_action(the_board,5,PLAYER1)
the_board = new_board
new_board = apply_player_action(the_board,5,PLAYER1)
the_board = new_board
print(new_board)
pretty_board = pretty_print_board(new_board)
print(pretty_board)
a=connected_four(new_board,PLAYER1)
print(a)
zio=check_end_state(new_board,PLAYER1)
print(zio)


def human_vs_agent(
    generate_move_1: GenMove,
    generate_move_2: GenMove = user_move,
    player_1: str = "Player 1",
    player_2: str = "Player 2",
    args_1: tuple = (),
    args_2: tuple = (),
    init_1: Callable = lambda board, player: None,
    init_2: Callable = lambda board, player: None,
):
    import time
    from game_utils import PLAYER1, PLAYER2, PLAYER1_PRINT, PLAYER2_PRINT, GameState
    from game_utils import initialize_game_state, pretty_print_board, apply_player_action, check_end_state

    players = (PLAYER1, PLAYER2)
    for play_first in (1, -1):
        for init, player in zip((init_1, init_2)[::play_first], players):
            init(initialize_game_state(), player)

        saved_state = {PLAYER1: None, PLAYER2: None}
        board = initialize_game_state()
        gen_moves = (generate_move_1, generate_move_2)[::play_first]
        player_names = (player_1, player_2)[::play_first]
        gen_args = (args_1, args_2)[::play_first]

        playing = True
        while playing:
            for player, player_name, gen_move, args in zip(
                players, player_names, gen_moves, gen_args,
            ):
                t0 = time.time()
                print(pretty_print_board(board))
                print(
                    f'{player_name} you are playing with {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
                )
                action, saved_state[player] = gen_move(
                    board.copy(), player, saved_state[player], *args
                )
                print(f"Move time: {time.time() - t0:.3f}s")
                board = apply_player_action(board, action, player)
                end_state = check_end_state(board, player)
                if end_state != GameState.STILL_PLAYING:
                    print(pretty_print_board(board))
                    if end_state == GameState.IS_DRAW:
                        print("Game ended in draw")
                    else:
                        print(
                            f'{player_name} won playing {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
                        )
                    playing = False
                    break


if __name__ == "__main__":
    human_vs_agent(user_move)