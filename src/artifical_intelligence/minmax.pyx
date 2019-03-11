
"""
Calculate the next move to make using the minmax algorithm
input: 
    - state: instance of the game state
    - profondeur: maximum depth of exploration
    - 
"""
def minmax_gen(state, profondeur, scoring_function, player, getNextStates):
    # on est sur une feuille
    if profondeur == 0:
        return (state, scoring_function(state))
    else:
        next_states = getNextStates(state)
        if player == "max":
            bestState = None
            bestScore = -10000
            for next_state in next_states:
                next_best_state, score = minmax_gen(next_state, profondeur-1, scoring_function, "min", getNextStates)
                if score > bestScore:
                    bestScore = score
                    bestState = next_best_state
            return (bestState, bestScore)
        elif player == "min":
            bestState = None
            bestScore = 10000
            for next_state in next_states:
                next_best_state, score = minmax_gen(next_state, profondeur-1, scoring_function, "max", getNextStates)
                if score < bestScore:
                    bestScore = score
                    bestState = next_best_state
            return (bestState, bestScore)

def minmax(state, profondeur, scoring_function, getNextStates):
    return minmax_gen(state, profondeur, scoring_function, "max", getNextStates)