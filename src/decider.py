from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
from artifical_intelligence.meta_heuristic import *
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE, MIN_SPLIT


SPLIT_MODE = 0
SIMPLE_GAME = 1
NO_SPLIT_GAME = 2
"""
take a game state and return the next moves

"""
def next_states_split(state):
        return get_next_states(state, True)
    

def next_moves_decider(game_state):
    def scoring(state):
        #return scoring_function(state, game_state.team_specie, 20, -3, 1)
        return scoring_function_2(state, game_state.team_specie, 20, -20, 10)

    
    print("Deciding move for specie " + str(game_state.team_specie))

    mode = NO_SPLIT_GAME
    #### META HEURISTIC
    if game_state.team_specie == VAMPIRE:
        ennemies = game_state.werewolves
        users_count = game_state.vampire_count
    else:
        ennemies = game_state.vampires
        users_count = game_state.werewolf_count
    
    is_split_good = True

    if len(game_state.humans) + len(ennemies) < 6 and users_count == 1:
        mode = SIMPLE_GAME
    if is_split_good:
        mode = SPLIT_MODE
    else:
        mode = NO_SPLIT_GAME
    #### END META HEURISTIC


    if mode == SPLIT_MODE:
        profondeur = 2
        moves, bestScore = alphabeta(game_state, profondeur, scoring, next_states_split)
    elif mode == SIMPLE_GAME:
        profondeur = 8
        moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states)
    else: # mode == NO_SPLIT_GAME
        profondeur = 4
        moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states)
    
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    for m in moves:
        print(m)
    return moves
