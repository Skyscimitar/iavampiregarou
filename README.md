# iavampiregarou
__Groupe 8__

IA pour jouer au jeu des loup-garous contre les vampires

## Venv

```
python3 -m venv venv
source ./venv/bin/activate
deactivate

```

## Project structure
*  connectionServer.py : Connect to server. Receive and send commands
*  game_state : 
	*  GameState.py : create a gamestate (=record of the map with the positions of all species in it)
	*  constants.py : file registering the value for variable including the maximum number of group and minimum split
	*  next.py : give all the next state possible after receiving a gamestate  [Do we use it ? To remove ?]
*  decider.py : return the next move after receiving a gamestate according to whether or not the split mode is activated
*  test-perf.py : file to test how much time a copy of gamestate takes [To remove]
*  artificial_intelligence :
	*  alphabeta.py :Returns list of changes to make using alphabeta version of the minimax algorithm
	*  minmax.py : Calculate the next move from a gameState using the minmax algorithm 
	*  coring_function.py : Calculate the score for a gameState

## Steps

### 1. Connection to Server
Launch connectionServer.py using the invite de commande [tmtc] with the structure 
Python connectionServer.py 123.123.3.5 6666 		(123.123.3.5 being the host IP and 6666 being the port to connect)


### 2. Initialize Game State
Thanks to the information received from Server via connectionServer.py a GameState is created using GameState.py

### 3. Calculate all next move possible


### 4. Score all the next move

### 5. Send the move with the highest score



