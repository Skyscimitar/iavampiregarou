

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
        next_states = getNextStates(state)
        if player == "max":
            bestState = None
            bestScore = -10000
            for next_state in next_states:
                next_best_state, score = alphabeta_gen(next_state, profondeur-1, scoring_function, "min", getNextStates, alpha, beta)
                if score > bestScore:
                    alpha = max(alpha, score)
                    bestScore = score
                    bestState = next_best_state
                if alpha >= beta:
                    return (bestState, bestScore)
            return (bestState, bestScore)
        elif player == "min":
            bestState = None
            bestScore = 10000
            for next_state in next_states:
                next_best_state, score = alphabeta_gen(next_state, profondeur-1, scoring_function, "max", getNextStates, alpha, beta)
                if score < bestScore:
                    beta = min(beta, score)
                    bestScore = score
                    bestState = next_best_state
                if alpha >= beta:
                    return (bestState, bestScore)
            return (bestState, bestScore)

def alphabeta(state, profondeur, scoring_function, getNextStates):
    return alphabeta_gen(state, profondeur, scoring_function, "max", getNextStates)