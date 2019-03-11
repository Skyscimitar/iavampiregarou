from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE, MIN_SPLIT
"""
take a game state and return the next moves

"""
def next_moves_decider(game_state):
    def scoring(state):
        #return scoring_function(state, game_state.team_specie, 20, -3, 1)
        return scoring_function_2(state, game_state.team_specie, 20, -20, 1)

    def next_states_split(state):
        return get_next_states(state, True)
    
    print("Deciding move for specie " + str(game_state.team_specie))
    if game_state.team_specie == VAMPIRE:
        ennemies = game_state.werewolves
        users = game_state.vampires
    else:
        ennemies = game_state.vampires
        users = game_state.werewolves
    
    is_split_good = True
    if is_split_good:
        profondeur = 1
        next_state_function = next_states_split
    elif len(game_state.humans) + len(ennemies) < 6 and len(users) == 1:
        profondeur = 8
        next_state_function = get_next_states
    else:
        next_state_function = get_next_states
        profondeur = 4
    

    moves, bestScore = alphabeta(game_state, profondeur, scoring, next_state_function)
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    for m in moves:
        print(m)
    return moves
