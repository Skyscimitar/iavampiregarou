import itertools
from time import sleep,time
from game_state.GameState import *
from copy import deepcopy

game = GameState(20, 20)

start = time()
for i in range(64*64):
    game2 = deepcopy(game)
end = time()
print("Done in {0} seconds".format( end - start))

game = GameState(40, 40)
start = time()
for i in range(64*64):
    game2 = deepcopy(game)
end = time()
print("Done in {0} seconds".format( end - start))