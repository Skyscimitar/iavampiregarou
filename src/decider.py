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
        return scoring_function_2(state, game_state.team_specie, 20, -20)
    
    print("Deciding move for specie " + str(game_state.team_specie))
    if game_state.team_specie == VAMPIRE:
        ennemies = game_state.werewolves
    else:
        ennemies = game_state.vampires
    
    profondeur = 4
    if len(game_state.humans) + len(ennemies) < 6:
        profondeur = 8

    moves, bestScore = alphabeta(game_state, profondeur, scoring, get_next_states)
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    for m in moves:
        print(m)
    return moves
