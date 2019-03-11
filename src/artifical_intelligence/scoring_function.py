import numpy as np
import sys
sys.path.append('..')
from game_state.constants import HUMAN, WEREWOLF, VAMPIRE

"""
Scoring_function, calculate the score of an instance of the game state
input: 
    gameState - an instance of the game state
    alpha: weight given to our team
    beta: weight given to the opponent's team
    gamma: weight given to human camps
output: 
    score: int - the score the game state has using the provided heuristic function.
"""
def scoring_function(gameState, player_to_maximize, alpha, beta, gamma):
    vampires = gameState.vampires
    werewolves = gameState.werewolves
    humans = gameState.humans
    remaining_moves = float(gameState.remaining_moves)

    if player_to_maximize == VAMPIRE:
        users = vampires
    else:
        users = werewolves

    h_score = 0
    for user in users:
        for human in humans:
            if user.number >= human.number:
                if distance(user, human) > 0 :
                    h_score += float(gamma*human.number)/distance(user, human)
    if player_to_maximize == VAMPIRE:
        return alpha*gameState.vampire_count + beta*gameState.werewolf_count + h_score*(remaining_moves/200)
    else:
        return beta*gameState.vampire_count + alpha*gameState.werewolf_count + h_score*(remaining_moves/200)



def distance(entity_1, entity_2):
    return max(np.abs(entity_1.x - entity_2.x), np.abs(entity_1.y - entity_2.y))
    

def scoring_function_2(gameState, player_to_maximize, alpha, beta, gamma):
    # vampires = gameState.vampires
    # werewolves = gameState.werewolves
    humans = gameState.humans
    remaining_moves = gameState.remaining_moves
    max_moves = 200

    if player_to_maximize == VAMPIRE:
        users = gameState.vampires
        users_count = gameState.vampire_count
        ennemies = gameState.werewolves
        ennemies_count = gameState.werewolf_count
    else:
        users = gameState.werewolves
        users_count = gameState.werewolf_count
        ennemies = gameState.vampires
        ennemies_count = gameState.vampire_count

    # h_score = nearest_human_camp(humans, users, ennemies, gamma)
    # h_score = 0
    k_score = kill_score(users, ennemies, 0.1)
    # bh_score = humans_barycentre(humans, users, 0.4)
    h_bh_score = optimised_near_human_barycentre(users, ennemies, humans, 0.4, gamma)
    end_score = kill_end_game(gameState.human_count, users, ennemies, 200)
    # split_score = number_groups_scores(users, len(humans), 10)
    split_score = 0 
    #end_score = 0

    return alpha*users_count + beta*ennemies_count + k_score + h_bh_score + end_score + split_score


def nearest_human_camp(humans, users, ennemies, gamma):
    h_score = 0
    for human in humans:

        min_distance_possible_user = 1000
        for u in users:
            if distance(u, human) < min_distance_possible_user and u.number >= human.number:
                min_distance_possible_user = distance(u, human)
        
        min_distance_possible_ennemy = 1000
        for v in ennemies:
            if distance(v, human) < min_distance_possible_user and v.number >= human.number:
                min_distance_possible_user = distance(v, human)

        if min_distance_possible_user < min_distance_possible_ennemy:
            # gamma = 10
            h_score += gamma*human.number/min_distance_possible_user
        else :
            # gamma = -10
            h_score += -gamma*human.number/min_distance_possible_ennemy
    
    return h_score

def humans_barycentre(humans, users, alpha):
    bh_score = 0
    for user in users:
        for human in humans:
            if user.number >= human.number:
                if distance(user, human) > 0 :
                    bh_score += float(human.number)/distance(user, human)
    return alpha*bh_score

def kill_score(users, ennemies, alpha):
    k_score = 0
    for u in users:
        for v in ennemies:
            if v.number*1.5 < u.number:
                k_score += v.number/distance(u, v)
    return alpha*k_score


def kill_end_game(human_count, users, ennemies, alpha):
    if human_count == 0:
        if len(ennemies) == 0:
            return 2000*alpha
        if len(users) == 1 and len(ennemies) == 1 and users[0].number < ennemies[0].number:
            return float(alpha)/distance(users[0], ennemies[0])
    return 0


def number_groups_scores(users, nb_human_camp, param):
    if len(users) == 1:
        return 0
    else:
        if nb_human_camp == 0:
            param = 10*param
        else:
            param = 0
        total_distance = 0
        for i in range(len(users)):
            for j in range(i, len(users)):
                total_distance += distance(users[i], users[j])
        return -param*(len(users) + total_distance)

def optimised_near_human_barycentre(users, ennemies, humans, alpha_bar, alpha_h):
    h_score = 0
    bh_score = 0
    for human in humans:

        min_distance_possible_user = 1000
        for u in users:
            if u.number >= human.number:
                dist_u_h = distance(u, human)
                if dist_u_h > 0 :
                    bh_score += float(human.number)/dist_u_h
                if dist_u_h < min_distance_possible_user:
                    min_distance_possible_user = dist_u_h
        
        min_distance_possible_ennemy = 1000
        for v in ennemies:
            if distance(v, human) < min_distance_possible_user and v.number >= human.number:
                min_distance_possible_user = distance(v, human)

        if min_distance_possible_user < min_distance_possible_ennemy:
            # gamma = 10
            h_score += alpha_h*human.number/min_distance_possible_user
        else :
            # gamma = -10
            h_score += -alpha_h*human.number/min_distance_possible_ennemy
    
    return h_score + alpha_bar*bh_score