

"""
Indicates if the game is over or not
input: game_state: GameState
output: bool
"""
def terminal_test(game_state):
    return game_state.check_game_over()

"""
Returns list of changes to make using alphabeta version of the minimax algorithm
input: game_state: GameState, depth: int, scoring_function: (game_state: GameState) -> float
output: [(xi:int, yi:int, nb_individus:int, xo:int, yo:int)]
"""
def alphabeta(game_state, depth, scoring_function):
    return True

