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

connectionServer.py : Connect to server. Receive and send commands
game_state : 
	GameState.py : create a gamestate (=record of the map with the positions of all species in it)
	constants.py : file registering the value for variable including the maximum number of group and minimum split
	next.py : give all the next state possible after receiving a gamestate  [Do we use it ? To remove ?]

