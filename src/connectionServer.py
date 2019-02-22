import socket
from time import sleep
from src.game_state import *

import struct
from src.artifical_intelligence import next_moves_decider

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
    #print(movements)

    for movement in movements:
        paquet += bytes([movement[0]])
        paquet += bytes([movement[1]])
        paquet += bytes([movement[2]])
        paquet += bytes([movement[3]])
        paquet += bytes([movement[4]])


    sock.send(paquet)


if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    print('Connecté')
    send_nme_command(sock, 'helene')




    while True :
        cmd = getcommand(sock)
        #print('commande reçue :' + cmd )
        if cmd == u"SET":
            n,m = understand_set_command(sock)
            game = GameState(n,m)
        elif cmd == u"HUM":
            print("HUM command:", understand_hum_command(sock))
        elif cmd == u"HME":
            print("HME command:", understand_hme_command(sock))
        elif cmd == u"MAP":
            map = understand_upd_command(sock)
            for case in map :
                game.set_cell(case)
        elif cmd == u"UPD":
            upd = understand_upd_command(sock)
            for change in upd :
                game.set_cell(change)
            moves = next_moves_decider()
            send_mov_command(sock, moves)
        elif cmd == u"END":
            break
        elif cmd == u"BYE":
            sleep(1)
            continue
        else:
            raise ValueError("Erreur protocole")
