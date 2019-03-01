from artifical_intelligence.alphabeta import alphabeta
from game_state.GameState import get_next_states
from game_state.next import stupidNext
from artifical_intelligence.scoring_function import scoring_function, scoring_function_2
"""
take a game state and return the next moves

"""
def next_moves_decider(game_state):
    def scoring(state):
        return scoring_function(state, 3, -3, 1)
        #return scoring_function_2(state, -1.2)
    moves, bestScore = alphabeta(game_state, 5, scoring, get_next_states)
    #moves, bestScore = alphabeta(game_state, 5, scoring, stupidNext)
    print("next move decided with alpha beta score:" + str(bestScore) + "  move:" + str(moves))
    return moves
