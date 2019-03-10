import sys
sys.path.append('..')
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE
from game_state.GameState import print_map

"""
Returns list of changes to make using alphabeta version of the minimax algorithm
input: game_state: GameState, depth: int, scoring_function: (game_state: GameState) -> float
output: [(xi:int, yi:int, nb_individus:int, xo:int, yo:int)]
"""

def alphabeta_gen(state, profondeur, scoring_function, player, getNextStates, alpha, beta):
    # on est sur une feuille
    if profondeur == 0:
        return (state, scoring_function(state))
    else:
        next_states, moves = getNextStates(state, True)
        #print("moves ", len(state.vampires), len(moves), moves, len(next_states))
        #print()
        if player == "max":
            bestMove = None
            bestScore = -100000000000000
            for i, next_state in enumerate(next_states):
                next_best_state, score = alphabeta_gen(next_state, profondeur-1, scoring_function, "min", getNextStates, alpha, beta)
                if score > bestScore:
                    alpha = max(alpha, score)
                    bestScore = score
                    bestMove = moves[i]
                if alpha >= beta:
                    return (bestMove, bestScore)
            return (bestMove, bestScore)
        elif player == "min":
            bestMove = None
            bestScore = 100000000000000
            for i, next_state in enumerate(next_states):
                next_best_state, score = alphabeta_gen(next_state, profondeur-1, scoring_function, "max", getNextStates, alpha, beta)
                if score < bestScore:
                    beta = min(beta, score)
                    bestScore = score
                    bestMove = moves[i]
                if alpha >= beta:
                    return (bestMove, bestScore)
            return (bestMove, bestScore)

def alphabeta(state, profondeur, scoring_function, getNextStates):
    print("Starting alpha beta with map")
    print_map(state)
    return alphabeta_gen(state, profondeur, scoring_function, "max", getNextStates, -10000, 10000)