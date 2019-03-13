import sys
sys.path.append('..')
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE
from game_state.GameState import print_map
import g_var

"""
Returns list of changes to make using alphabeta version of the minimax algorithm
input: game_state: GameState, depth: int, scoring_function: (game_state: GameState) -> float
output: [(xi:int, yi:int, nb_individus:int, xo:int, yo:int)]
"""

def sort_game_func(game, scoring_func):
    return scoring_func(game)

def alphabeta_gen(state, event_stop, profondeur, scoring_function, player, getNextStates, alpha, beta, profondeur_initiale):
    # on est sur une feuille
    if profondeur == 0:
        return (state, scoring_function(state))
    else:
        next_states, moves = getNextStates(state)
        #print("moves ", len(state.vampires), len(moves), moves, len(next_states))
        #print()
        if player == "max":
            bestMove = None
            bestScore = -100000000000000
            # guiding search
            if profondeur_initiale == profondeur:
                couplage = [(next_states[i], moves[i]) for i in range(len(moves))]
                couplage_sorted = sorted(couplage, key = lambda x: sort_game_func(x[0], scoring_function), reverse=True)
                next_states = [x[0] for x in couplage_sorted]
                moves = [x[1] for x in couplage_sorted]

            for i, next_state in enumerate(next_states):
                next_best_state, score = alphabeta_gen(next_state, event_stop, profondeur-1, scoring_function, "min", getNextStates, alpha, beta, profondeur_initiale)
                if event_stop.is_set():
                    return (bestMove, bestScore)
                
                if score > bestScore:
                    alpha = max(alpha, score)
                    bestScore = score
                    bestMove = moves[i]
                    if profondeur_initiale == profondeur and g_var.moves_computed != []:
                        print("assigning partial top var", bestMove)
                        g_var.moves_computed = bestMove
                if alpha >= beta:
                    return (bestMove, bestScore)
            return (bestMove, bestScore)
        elif player == "min":
            bestMove = None
            bestScore = 100000000000000

            for i, next_state in enumerate(next_states):
                next_best_state, score = alphabeta_gen(next_state, event_stop, profondeur-1, scoring_function, "max", getNextStates, alpha, beta, profondeur_initiale)
                if score < bestScore:
                    beta = min(beta, score)
                    bestScore = score
                    bestMove = moves[i]
                    if profondeur_initiale == profondeur and g_var.moves_computed != []:
                        # print("assigning partial top var", bestMove)
                        g_var.moves_computed = bestMove
                if alpha >= beta:
                    return (bestMove, bestScore)
            return (bestMove, bestScore)

def alphabeta(state, profondeur, scoring_function, getNextStates, event_stop):
    #print("Starting alpha beta with map")
    #print_map(state)
    return alphabeta_gen(state, event_stop, profondeur, scoring_function, "max", getNextStates, -10000, 10000, profondeur)