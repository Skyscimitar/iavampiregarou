import numpy as np

class GameState:


    def __init__(self, n, m):
        self.map = np.zeros((n,m))


    def set_species_on_cell(self, x, y, species, number):
        self.map[x][y] = (species, number)


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
    def check_game_over(species):
        game_over = True
        for i in self.map.shape[0]:
            for j in self.map.shape[1]:
                if self.map[i][j][0] == species and self.map[i][j] > 0:
                    game_over = False
                    break
        return game_over
        