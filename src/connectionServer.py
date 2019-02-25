import socket
from time import sleep
from game_state.GameState import *
import sys

from artifical_intelligence.decider import *

def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getint(sock):
    data = bytes()
    data += sock.recv(1)
    #print(data)
    return int.from_bytes(data, byteorder='big')


def understand_set_command(sock):
    n = getint(sock)
    m = getint(sock)
    return n, m


def understand_hum_command(sock):
    nb_homes = getint(sock)

    coordinates = []
    for i in range(nb_homes):
        x = getint(sock)
        y = getint(sock)
        coordinates += [(x,y)]

    return coordinates


def understand_hme_command(sock):
    x = getint(sock)
    y = getint(sock)

    return x,y


def understand_upd_command(sock):
    nb_changes = getint(sock)

    coordinates = []
    for i in range(nb_changes):
        x = getint(sock)
        y = getint(sock)
        humans = getint(sock)
        vampires = getint(sock)
        werewolves = getint(sock)
        coordinates += [(x,y,humans,vampires,werewolves)]

    return coordinates


def send_nme_command(sock, name):
    paquet = bytes()
    paquet += 'NME'.encode()
    paquet += bytes([len(name)])
    paquet += name.encode()
    sock.send(paquet)


def send_mov_command(sock, movements):
    paquet = bytes()
    paquet += 'MOV'.encode()
    paquet += bytes([len(movements)])
    for movement in movements:
        paquet += bytes([movement[0]])
        paquet += bytes([movement[1]])
        paquet += bytes([movement[2]])
        paquet += bytes([movement[3]])
        paquet += bytes([movement[4]])
    sock.send(paquet)


def play():
    if len(sys.argv) < 2 :
        print('Il manque des arguments')
        return
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))
    print('Connecté')
    send_nme_command(sock, 'helene')


    while True :
        cmd = getcommand(sock)
        #print('commande reçue :' + cmd )
        if cmd == u"SET":
            n,m = understand_set_command(sock)
            game = GameState(n,m)
        elif cmd == u"HUM":
            hum = understand_hum_command(sock)
        elif cmd == u"HME":
            hme = understand_hme_command(sock)
        elif cmd == u"MAP":
            map = understand_upd_command(sock)
            print(map)
            for case in map :
                game.convert_tuple(case)
                if case[0] == hme[0] and  case[1] == hme[1] :
                    if case[3] == 0 :
                        game.species = WEREWOLF
        elif cmd == u"UPD":
            upd = understand_upd_command(sock)
            for change in upd :
                game.convert_tuple(change)
            #print(game.map, game.humans, game.species)
            moves = next_moves_decider(game)
            send_mov_command(sock, moves)
        elif cmd == u"END":
            break
        elif cmd == u"BYE":
            sleep(1)
            continue
        else:
            raise ValueError("Erreur protocole")


if __name__ == '__main__':
    play()

