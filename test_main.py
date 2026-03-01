from main import get_config, get_bool, get_bot_move

def test_get_config():
    assert get_config("y", "PLAYER1_SYMBOL", "x") == "y"
    assert get_config("green", "PLAYER1_COLOR", "red") == "green"
    assert get_config(None, "NON_EXISTENT_ENV_VAR", "x") == "x"
    assert get_config(None, "ANOTHER_MISSING_VAR", "blue") == "blue"

def test_get_bool():
    assert get_bool(True, "REVERSED") is True
    assert get_bool(True, "INFINITE_GAMES") is True
    assert get_bool(False, "REVERSED") is False
    assert get_bool(False, "INFINITE_GAMES") is False

def test_get_bot_move():
    board_one_left = [0, "x", "o", "x", "o", 5, "x", "o", "x", "o"]
    assert get_bot_move(board_one_left, "simple") == 5

    board_win_o = [0, "o", "o", 3, "x", "x", 6, 7, 8, 9]
    assert get_bot_move(board_win_o, "minmax") == 3

    board_block_x = [0, "o", 2, 3, "x", "x", 6, 7, 8, 9]
    assert get_bot_move(board_block_x, "minmax") == 6

