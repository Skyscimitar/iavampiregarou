from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE, MIN_SPLIT


SPLIT_MODE = 0
SIMPLE_GAME = 1
NO_SPLIT_GAME = 2
"""
take a game state and return the next moves

"""
def get_next_states_split_func(game):
    def next_states_split(state):
        min_count_split = max(4,game.min_human_in_camp*2+1)
        return get_next_states(state, True, min_count_split=min_count_split)
    return next_states_split
    

def next_moves_decider(game_state, event_stop, deept_ajusted):
    def scoring(state):
        #return scoring_function(state, game_state.team_specie, 20, -3, 1)
        return scoring_function_2(state, game_state.team_specie, 20, -30, 8, 3)

    
    print("Deciding move for specie " + str(game_state.team_specie))

    mode = NO_SPLIT_GAME
    #### META HEURISTIC
    if game_state.team_specie == VAMPIRE:
        ennemies = game_state.werewolves
        users = game_state.vampires
    else:
        ennemies = game_state.vampires
        users = game_state.werewolves
    
    is_split_good = True

    if len(game_state.humans) + len(ennemies) <= 6 and len(users) == 1:
        mode = SIMPLE_GAME
    if is_split_good:
        mode = SPLIT_MODE
    else:
        mode = NO_SPLIT_GAME
    #### END META HEURISTIC


    if mode == SPLIT_MODE:
        profondeur = max(2, 7 - deept_ajusted)
        if len(game_state.humans) <= 1:
            profondeur = 2
        
        moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states_split_func(game_state), event_stop)
    elif mode == SIMPLE_GAME:
        profondeur = max(2, 8 - deept_ajusted)
        moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states, event_stop)
    else: # mode == NO_SPLIT_GAME
        profondeur = max(2, 4 - deept_ajusted)
        moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states, event_stop)
    
    # print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    # for m in moves:
    #     print(m)
    return moves
