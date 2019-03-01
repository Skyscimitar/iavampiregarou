import numpy as np
import sys
sys.path.append('..')
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE

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
def scoring_function(gameState, alpha, beta, gamma):
    vampires = gameState.vampires
    werewolves = gameState.werewolves
    humans = gameState.humans
    user_species = gameState.team_specie

    if user_species == VAMPIRE:
        users = vampires
    else:
        users = werewolves

    h_score = 0
    for user in users:
        for human in humans:
            if user.number > human.number:
                if distance(user, human) > 0 :
                    h_score += gamma*human.number/distance(user, human)
    if user_species == VAMPIRE:
        return alpha*gameState.vampire_count + beta*gameState.werewolf_count + h_score
    else:
        return beta*gameState.vampire_count + alpha*gameState.werewolf_count + h_score



def distance(entity_1, entity_2):
    return max(np.abs(entity_1.x - entity_2.x), np.abs(entity_1.y - entity_2.y))
    

def scoring_function_2(gameState, alpha):
    vampires = gameState.vampires
    werewolves = gameState.werewolves
    humans = gameState.humans
    user_species = gameState.team_specie

    if user_species == VAMPIRE:
        users = vampires
        ennemies = werewolves
    else:
        users = werewolves
        ennemies = vampires
    
    h_score = nearest_human_camp(humans, users, ennemies)

    if user_species == VAMPIRE:
        return gameState.vampire_count - gameState.werewolf_count + alpha*h_score
    else:
        return gameState.werewolf_count - gameState.vampire_count + alpha*h_score


def nearest_human_camp(humans, users, ennemies):
    h_score = 0
    for human in humans:
        min_distance_possible_user = 1000
        
        for u in users:
            if distance(u, human) < min_distance_possible_user and u.number > human.number:
                min_distance_possible_user = distance(u, human)
        
        min_distance_possible_ennemy = 1000
        for v in ennemies:
            if distance(v, human) < min_distance_possible_user and v.number > human.number:
                min_distance_possible_user = distance(v, human)
        if min_distance_possible_user < min_distance_possible_ennemy:
            h_score += human.number
    return h_score

