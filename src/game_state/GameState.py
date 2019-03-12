from .constants import HUMAN, WEREWOLF, VAMPIRE, MIN_SPLIT, MAX_GROUPES
from copy import deepcopy, copy
import itertools
import numpy as np

class GameState:


    def __init__(self, n, m):
        self.team_specie = VAMPIRE
        self.lines = n
        self.columns = m
        self.map = [[None for _ in range(m)] for a in range(n)]
        self.humans = []
        self.werewolves = []
        self.vampires = []
        self.vampire_count = 0
        self.werewolf_count = 0
        self.human_count = 0
        self.remaining_moves = 200


    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        result = copy(self)
        result.humans = copy(self.humans)
        result.map = copy(self.map)
        result.werewolves = copy(self.werewolves)
        result.vampires = copy(self.vampires)
        for i in range(len(result.map)):
            result.map[i] = copy(self.map[i])
        return result

def convert_tuple(gameState, tuple):
    x, y, humans, vampires, werewolves = tuple
    remove_specie_on_cell(gameState, x, y)
    if humans != 0:
        set_species_on_cell(gameState, x, y, HUMAN, humans)
    elif vampires != 0:
        set_species_on_cell(gameState, x, y, VAMPIRE, vampires)
    elif werewolves != 0:
        set_species_on_cell(gameState, x, y, WEREWOLF, werewolves)
    #else:
        #remove_specie_on_cell(gameState, x, y)
        #gameState.map[x][y] = None


def set_species_on_cell(gameState, x, y, species, number):
    # Les coordonnees de la map sont en mode [ordonnees] [abscisses]
    #print("Setting spec on cell " + str(x) + "," + str(y) + "  " + str(species) + " " + str(number))
    gameState.map[x][y] = MapEntity(number, species)
    entity = Entity(x, y, number)
    if species == HUMAN:
        gameState.humans.append(entity)
        gameState.human_count += entity.number
    elif species == VAMPIRE:
        gameState.vampires.append(entity)
        gameState.vampire_count += entity.number
    else:
        gameState.werewolves.append(entity)
        gameState.werewolf_count += entity.number


def remove_specie_on_cell(gameState, x, y):
    map_entity = gameState.map[x][y]
    #print("Removing cell " + str(x) + "," + str(y) + "  ", str(gameState.map[x][y]))
    #print("vampires before")
    #print_entity_list(gameState.vampires)
    if map_entity == None:
        return

    if map_entity.species == HUMAN:
        gameState.humans = [entity for entity in gameState.humans if (entity.x != x or entity.y != y)]
        gameState.human_count -= map_entity.number
    elif map_entity.species == VAMPIRE:
        gameState.vampires = [entity for entity in gameState.vampires if (entity.x != x or entity.y != y)]
        gameState.vampire_count -= map_entity.number
    else:
        gameState.werewolves = [entity for entity in gameState.werewolves if (entity.x != x or entity.y != y)]
        gameState.werewolf_count -= map_entity.number

    gameState.map[x][y] = None
    #print("vampires after")
    #print_entity_list(gameState.vampires)

def get_map_shape(gameState):
    return gameState.lines, gameState.columns


"""
Returns the species and number of inhabitants of a given cell
input: x: int, y: int
output: (species: int, number: int)
"""
def get_species_and_inhabitant_on_cell(gameState, x, y):
    return gameState.map[x][y]



def get_next_states(gameState, split=False, max_groupes=MAX_GROUPES):
    next_moves = []
    if gameState.team_specie == VAMPIRE:
        for vampire_group in gameState.vampires:
            adjacent_cells = get_interesting_adjacent_cells(gameState, vampire_group.x, vampire_group.y)
            next_moves_group = [None]
            next_moves_group += get_next_moves(gameState, vampire_group.x, vampire_group.y, vampire_group.number, adjacent_cells)
            if split and len(gameState.vampires) < max_groupes:
                split_moves = handle_split(gameState, vampire_group.x, vampire_group.y, vampire_group.number, adjacent_cells)
                next_moves_group += split_moves
            next_moves.append(list(next_moves_group))

        next_team_specie = WEREWOLF

    else:
        for werewolf_group in gameState.werewolves:
            adjacent_cells = get_interesting_adjacent_cells(gameState, werewolf_group.x, werewolf_group.y)
            next_moves_group = [None]
            next_moves_group += get_next_moves(gameState, werewolf_group.x, werewolf_group.y, werewolf_group.number, adjacent_cells)
            if split and len(gameState.werewolves) < max_groupes:
                split_moves = handle_split(gameState, werewolf_group.x, werewolf_group.y, werewolf_group.number, adjacent_cells)
                next_moves_group += split_moves
            next_moves.append(list(next_moves_group))

        next_team_specie = VAMPIRE

    possibles_combinations = itertools.product(*next_moves)
    final_combinations = []
    next_states = []

    for i, combo in enumerate(possibles_combinations):
        if i == 0:
            continue
        else:
            final_combos = []
            for movements in combo:
                if isinstance(movements, list):
                    for move in movements:
                        final_combos.append(move)
                else:
                    final_combos += [movements]

            final_combinations.append(final_combos)
            next_states.append(generate_state_from_moves(gameState, final_combos, next_team_specie))
    if final_combinations == []:
        return [gameState], [[]]
    return next_states, final_combinations


def generate_state_from_moves(gameState, combo, next_team_specie):
    newState = deepcopy(gameState)
    newState.team_specie = next_team_specie
    for move in combo:
        if move is not None:
            target_cell = get_species_and_inhabitant_on_cell(gameState, move.target_x, move.target_y)
            if target_cell is not None and target_cell.species == gameState.team_specie:
                set_species_on_cell(newState, move.target_x, move.target_y, move.target_specie, target_cell.number + move.target_count)
            else:
                remove_specie_on_cell(newState, move.target_x, move.target_y)
                set_species_on_cell(newState, move.target_x, move.target_y, move.target_specie, move.target_count)
            remove_specie_on_cell(newState, move.source_x, move.source_y)
    return newState






"""
Provides all the adjacent cells for a given state
input: x,y: int
output: adjacent_cells
"""
def get_adjacent_cells(gameState, x, y):
    adjacent_cells = []

    if x > 0:
        adjacent_cells.append((x - 1, y))

        if y > 0:
            adjacent_cells.append((x - 1, y - 1))

        if y < gameState.columns - 1:
            adjacent_cells.append((x - 1, y + 1))

    if x < gameState.lines - 1:
        adjacent_cells.append((x + 1, y))

        if y > 0:
            adjacent_cells.append((x + 1, y - 1))

        if y < gameState.columns - 1:
            adjacent_cells.append((x + 1, y + 1))

    if y > 0:
        adjacent_cells.append((x, y - 1))

    if y < gameState.columns - 1:
        adjacent_cells.append((x, y + 1))

    return adjacent_cells


"""
Provides all direction of interest
input: x,y: int
output: adjacent_cells
"""

def sign_f(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def get_cell_from_vector(x, y, v_x, v_y):
    abs_v_x = abs(v_x)
    abs_v_y = abs(v_y)
    if abs_v_x == abs_v_y and abs_v_x != 0: 
        return (x + sign_f(v_x), y + sign_f(v_y))
    elif abs_v_x > abs_v_y:
        return (x + sign_f(v_x), y)
    else:
        return (x, y + sign_f(v_y))

def get_interesting_adjacent_cells(gameState, x, y):
    interesting_adjacent_cells = []
    if gameState.team_specie == VAMPIRE:
        ennemies = gameState.werewolves
        users = gameState.vampires
    else:
        ennemies = gameState.vampires
        users = gameState.werewolves
    # si peu d'objet d'interet
    if (len(gameState.humans) + len(ennemies) <= 6 and len(users) == 1 ):
        return list(set([get_cell_from_vector(x, y, h.x - x, h.y -y) for h in gameState.humans+ennemies]))
    # normal process with adjacent cells
    else: 
        return get_adjacent_cells(gameState, x, y)


def get_next_moves(gameState, x, y, team_cell_population, adjacent_cells):
    #adjacent_cells = get_adjacent_cells(gameState, x, y)
    #print(adjacent_cells)
    #print("adjacent cells", len(adjacent_cells))

    movements = []
    for adj_x, adj_y in adjacent_cells:
        adjacent_cell = get_species_and_inhabitant_on_cell(gameState, adj_x, adj_y)

        if adjacent_cell is not None:
            adjacent_specie, adjacent_population = adjacent_cell.species, adjacent_cell.number
        else:
            adjacent_specie, adjacent_population = None, 0

        # listing the different scenarios
        if adjacent_specie == gameState.team_specie:
            # TODO: handle merge
            continue
        elif adjacent_population == 0:
            movements.append(
                [Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie, team_cell_population)])
        else:
            # TODO: gerer les batailles aleatoires
            # Pour l'instant, on va la ou on est sur de gagner
            if adjacent_specie == HUMAN:
                if team_cell_population >= adjacent_population:
                    movements = [[Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie, team_cell_population + adjacent_population)]] + movements
            else:
                if team_cell_population >= 1.5 * adjacent_population:
                    movements = [[Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie, team_cell_population)]] + movements
                else:
                    if gameState.team_specie == VAMPIRE:
                        team_count = gameState.vampire_count
                        enemy_count = gameState.werewolf_count
                    else:
                        team_count = gameState.werewolf_count
                        enemy_count = gameState.vampire_count
                    
                    if team_count + gameState.human_count < enemy_count:
                        # TODO: verifier la probabilite
                        probability = team_cell_population / adjacent_population - 0.5
                        movements = [[Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie,
                                     round(probability * team_cell_population, 0))]] + movements
                    elif team_cell_population >= adjacent_population:
                        if team_count < enemy_count + gameState.human_count:
                            probability = team_cell_population / adjacent_population - 0.5
                            movements = [[Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie, round(probability * team_cell_population, 0))]] + movements

                    #movements = [Movement(x, y, team_cell_population, adj_x, adj_y, gameState.team_specie, team_cell_population)] + movements
    
    return movements

"""
Gives the result of a fight between a number attackers_count of attackers and a number defenders_count of defenders
If random fight, the survivor count is the expected count of survivors
input: attackers_count, defenders_count, defenders_specie: int
output: [(victory, survivor_count, probability),...]: array of possible states as 3-tuples with
    - victory: boolean (True if attackers won)
    - survivor_count: int
    - probability: float (probability of this state to happen)
"""
def fight_aleatoire(attackers_count, defenders_count, defenders_specie):

    if defenders_specie == HUMAN:
        if attackers_count >= defenders_count:
            return [(True, attackers_count + defenders_count, 1)]

        probability = attackers_count / (2 * defenders_count)
        inverse_probability = 1 - probability

        # TODO: etudier s il est vraiment intelligent de renvoyer le second cas
        return [
            (True, round((attackers_count + defenders_count) * probability, 0), probability),
            (False, round(inverse_probability * defenders_count, 0), inverse_probability)
        ]

    # If attack on other specie
    if attackers_count >= 1.5 * defenders_count:
        return [(True, attackers_count, 1)]
    elif attackers_count <= defenders_count:
        probability = attackers_count / (2 * defenders_count)
        inverse_probability = 1 - probability
    else:
        probability = attackers_count / defenders_count - 0.5
        inverse_probability = 1 - probability

    # TODO: etudier s il est vraiment intelligent de renvoyer le second cas
    return [
        (True, round(attackers_count * probability, 0), probability),
        (False, round(inverse_probability * defenders_count, 0), inverse_probability)
        ]


def print_map(state):
    print('[', end='')
    for i in range(state.lines):
        print("[", end='')
        for j in range(state.columns):
            print(state.map[i][j], end=', ')
        print("]")
    print("]")
    print("Additionnal info")
    print("vampires: ")
    for v in state.vampires:
        print(v, end=', ')
    print("#")
    print("werewolves")
    for v in state.werewolves:
        print(v, end=', ')
    print("#")
    print("humans")
    for v in state.humans:
        print(v, end=', ')
    print("#")

def print_entity_list(l):
    print('[', end='')
    for e in l:
        print(e, end=', ')
    print(']')

class Entity:

    def __init__(self, x, y, number):
        self.number = number
        self.x = x
        self.y = y

    def __str__(self):
        return "x:" + str(self.x) + " y:" + str(self.y) + "  n:" + str(self.number);


class MapEntity:

    def __init__(self, number, species):
        self.number = number
        self.species = species

    def __str__(self):
        return "n:" +str(self.number) + " s:" + str(self.species)


def handle_split(gameState, x, y, team_cell_population, adjacent_cells, min_count=10):
    if team_cell_population < 2*min_count:
        return []
    population_1 = min_count
    population_2 = team_cell_population - min_count
    movements_1 = get_next_moves(gameState, x, y , population_1, adjacent_cells)
    movements_2 = get_next_moves(gameState, x, y, population_2, adjacent_cells)
    movements = itertools.product(*[movements_1, movements_2])
    final_movements = []
    for i, movement in enumerate(movements):
        if check_movement_destinations(movement[0][0], movement[1][0]):
            continue
        else:
            final_movements.append([movement[0][0], movement[1][0]])
    return final_movements
    


def get_stupid_valid_move(gameState):
    if gameState.team_specie == VAMPIRE:
        entity = gameState.vampires[0]
        adj_x, adj_y = get_adjacent_cells(gameState, entity.x, entity.y)[0]
        return [Movement(entity.x, entity.y, entity.number, adj_x, adj_y, None, None)]
    else:
        entity = gameState.werewolves[0]
        adj_x, adj_y = get_adjacent_cells(gameState, entity.x, entity.y)[0]
        return [Movement(entity.x, entity.y, entity.number, adj_x, adj_y, None, None)]

        


    



class Movement:

    def __init__(self, source_x, source_y, units_moved_count, target_x, target_y, target_specie, target_count):
        self.source_x = source_x
        self.source_y = source_y
        self.units_moved_count = units_moved_count
        self.target_x = target_x
        self.target_y = target_y
        self.target_specie = target_specie
        self.target_count = target_count

    def __str__(self):
        return "Movement: [ s_x:" + str(self.source_x) + ", s_y:" + str(self.source_y) + ", nb_unit:" + \
             str(self.units_moved_count) + ", t_x:" + str(self.target_x) + ", t_y:" + str(self.target_y) + "]"


def check_movement_destinations(movement_1, movement_2):
    if movement_1.target_x == movement_2.target_x and movement_1.target_y == movement_2.target_y:
        return True
    return False