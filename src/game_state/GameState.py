import numpy as np
from .constants import HUMAN, WEREWOLF, VAMPIRE

class GameState:


    def __init__(self, n, m):
        self.species = VAMPIRE
        self.n = n
        self.m = m
        self.map = [[None for _ in range(m)] for _ in range(n)]
        self.humans = []
        self.werewolves = []
        self.vampires = []
        self.vampire_count = 0
        self.werewolf_count = 0
        self.human_count = 0

    def convert_tuple (self, tuple) :
        x, y, humans, vampires, werewolves = tuple
        if humans != 0 :
            self.set_species_on_cell(x,y, HUMAN, humans)
        elif vampires != 0 :
            self.set_species_on_cell(x,y, VAMPIRE, vampires)
        elif werewolves != 0:
            self.set_species_on_cell(x,y, WEREWOLF, werewolves)
        else :
            self.map[y][x] = None


    def set_species_on_cell(self, x, y, species, number):
        #Les coordonnées de la map sont en mode [ordonnées] [abscisses]
        self.map[y][x] = (species, number)
        entity = Entity(x,y,number)
        if species == HUMAN:
            self.humans.append(entity)
            self.human_count += entity.number
        elif species == VAMPIRE:
            self.vampires.append(entity)
            self.vampire_count += entity.number
        else:
            self.werewolves.append(entity)
            self.werewolf_count += entity.number


    def get_map_shape(self):
        return (self.n, self.m)

    """
    Returns the species and number of inhabitants of a given cell
    input: x: int, y: int
    output: (species: string, number: int)
    """
    def get_species_and_inhabitant_on_cell(self, x, y):
        return self.map[x][y]

    
    """
    Checks if the game is over (no more of the player's species on the board)
    input: species: string
    ouptut: bool
    """
    def check_game_over(self, species):
        game_over = True
        for i in self.map.shape[0]:
            for j in self.map.shape[1]:
                if self.map[i][j][0] == species and self.map[i][j] > 0:
                    game_over = False
                    break
        return game_over
        

class Entity:

    def __init__(self, x, y, number):
        self.number = number
        self.x = x
        self.y = y


class MapEntity:

    def __init__(self, number, species):
        self.number = number
        self.species = species