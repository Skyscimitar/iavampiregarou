import numpy as np
from src.game_state import HUMAN, WEREWOLF, VAMPIRE

"""
Scoring_function, calculate the score of an instance of the game state
input: 
    gameState - an instance of the game state
    alpha: weight given to the vampire population
    beta: weight given to the werewolf population
    gamma: weight given to human camps
output: 
    score: int - the score the game state has using the provided heuristic function.
"""
def scoring_function(gameState, alpha, beta, gamma , user_species):
    vampires = gameState.vampires
    werewolves = gameState.werewolves
    humans = gameState.humans

    if user_species == VAMPIRE:
        users = vampires
    else:
        users = werewolves

    h_score = 0
    for user in users:
        for human in humans:
            if user.number > human.number:
                h_score += gamma*human.number/distance(user, human)
    return alpha*gameState.vampires + beta*gameState.werewolves + h_score



def distance(entity_1, entity_2):
    return np.abs(entity_1.x - entity_2.x) + np.abs(entity_1.y - entity_2.y)
    
