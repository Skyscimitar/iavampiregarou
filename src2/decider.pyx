from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
"""
take a game state and return the next moves

"""
def next_moves_decider(game_state):
    def scoring(state):
        #return scoring_function(state, game_state.team_specie, 20, -3, 1)
        return scoring_function_2(state, game_state.team_specie, 20, -20)
    print("Deciding move for specie " + str(game_state.team_specie))
    moves, bestScore = alphabeta(game_state, 4, scoring, get_next_states)
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:")
    for m in moves:
        print(m)
    return moves