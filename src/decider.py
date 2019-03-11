from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
from artifical_intelligence.meta_heuristic import *
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE, MIN_SPLIT
"""
take a game state and return the next moves

"""
def next_moves_decider(game_state):
    def scoring(state):
        #return scoring_function(state, game_state.team_specie, 20, -3, 1)
        return scoring_function_2(state, game_state.team_specie, 20, -20, 10)

    def next_states_split(state):
        return get_next_states(state, True)
    
    print("Deciding move for specie " + str(game_state.team_specie))

    mode = get_game_mode(game_state)
    
    if mode == SPLIT_MODE:
        profondeur = 2
        next_state_function = next_states_split
    elif mode == SIMPLE_GAME:
        profondeur = 5
        next_state_function = get_next_states
    else: # mode == NO_SPLIT_GAME
        next_state_function = get_next_states
        profondeur = 4
    
    

    moves, bestScore = alphabeta(game_state, profondeur, scoring, next_state_function)
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    for m in moves:
        print(m)
    return moves
