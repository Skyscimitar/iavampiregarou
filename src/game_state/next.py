from copy import deepcopy
from .constants import HUMAN, WEREWOLF, VAMPIRE
from .GameState import Entity, set_species_on_cell, remove_specie_on_cell, print_map,Movement

def stupidNext(gameState):
    # on split jamais, on a toujours seulement une seule case
    #print("Finding next State based on :")
    #print_map(gameState)

    nexts = []
    moves = []
    vampires = gameState.vampires
    werewolves = gameState.werewolves
    humans = gameState.humans

    # Si pas de test sur la longueur, on plante si on tue tous les autres !
    if gameState.team_specie == VAMPIRE and len(vampires) > 0:
        # and len(vampires) > 0
        user = vampires[0]
        ennemies = werewolves
        ENNEMY = WEREWOLF
    elif len(werewolves) > 0:
        user = werewolves[0]
        ennemies = vampires
        ENNEMY = VAMPIRE
    else:
        return [], []

    for i in range(3):
        for j in range(3):
            if ((i != 1 or j != 1) and 0 <= user.y + j - 1 and user.y + j - 1 < gameState.columns and 0 <= user.x + i - 1 and user.x + i - 1 < gameState.lines):
                gameState2 = deepcopy(gameState)
                if (gameState2.map[user.x + i - 1][user.y + j - 1] == None ):
                    set_species_on_cell(gameState2,  user.x + i - 1, user.y + j - 1, gameState.team_specie, user.number)
                    remove_specie_on_cell(gameState2, user.x, user.y)
                    gameState2.team_specie = ENNEMY
                    gameState2.remaining_moves -= 1
                    moves += [[Movement(user.x, user.y, user.number, user.x + i - 1, user.y + j - 1,None,None)]]
                    nexts += [gameState2]
                elif (gameState2.map[user.x + i - 1][user.y + j - 1].species == ENNEMY and gameState2.map[user.x + i - 1][user.y + j - 1].number*1.5 < user.number ):
                    remove_specie_on_cell(gameState2, user.x + i - 1, user.y + j - 1)
                    set_species_on_cell(gameState2, user.x + i - 1, user.y + j - 1, gameState.team_specie, user.number)
                    remove_specie_on_cell(gameState2, user.x, user.y)
                    gameState2.team_specie = ENNEMY
                    gameState2.remaining_moves -= 1
                    moves += [[Movement(user.x, user.y, user.number, user.x + i - 1, user.y + j - 1,None,None)]]
                    nexts += [gameState2]
                elif (gameState2.map[user.x + i - 1][user.y + j - 1].species == HUMAN and gameState2.map[user.x + i - 1][user.y + j - 1].number <= user.number ):
                    nb_humans = gameState2.map[user.x + i - 1][user.y + j - 1].number
                    remove_specie_on_cell(gameState2, user.x + i - 1, user.y + j - 1)
                    set_species_on_cell(gameState2, user.x + i - 1, user.y + j - 1, gameState.team_specie, user.number + nb_humans)
                    remove_specie_on_cell(gameState2, user.x, user.y)
                    gameState2.team_specie = ENNEMY
                    gameState2.remaining_moves -= 1
                    moves += [[Movement(user.x, user.y, user.number, user.x + i - 1, user.y + j - 1,None,None)]]
                    nexts += [gameState2]
    """
    print("nextsStupid ", len(nexts), "moves", len(moves))
    print("1er Next state ")
    print_map(nexts[0])
    print("moves")
    print(moves[0])
    """


    return nexts, moves
                
                

