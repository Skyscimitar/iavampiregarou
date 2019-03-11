import sys
sys.path.append('..')
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE

SPLIT_MODE = 0
SIMPLE_GAME = 1
NO_SPLIT_GAME = 2

"""
    return a mode among the above
"""
def get_game_mode(game_state):
    if game_state.team_specie == VAMPIRE:
        ennemies = game_state.werewolves
        users_count = game_state.vampire_count
    else:
        ennemies = game_state.vampires
        users_count = game_state.werewolf_count
    
    is_split_good = True

    if len(game_state.humans) + len(ennemies) < 6 and users_count == 1:
        return SIMPLE_GAME
    if is_split_good:
        return SPLIT_MODE
    else:
        return NO_SPLIT_GAME