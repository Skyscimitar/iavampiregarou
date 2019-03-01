import socket
from time import sleep,time
from game_state.GameState import *
import sys

from decider import next_moves_decider

def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getint(sock):
    data = bytes()
    data += sock.recv(1)
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
        # reverse x and y
        # y = getint(sock)
        # x = getint(sock)
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
        paquet += bytes([movement.source_x])
        paquet += bytes([movement.source_y])
        paquet += bytes([movement.units_moved_count])
        paquet += bytes([movement.target_x])
        paquet += bytes([movement.target_y])
    sock.send(paquet)


def play():
    if len(sys.argv) < 2 :
        print('Il manque des arguments')
        return
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))
    print('Connecte')
    send_nme_command(sock, 'helene')


    while True :
        cmd = getcommand(sock)
        #print('commande recue :' + cmd )
        if cmd == u"SET":
            n,m = understand_set_command(sock)
            game = GameState(m, n)
        elif cmd == u"HUM":
            hum = understand_hum_command(sock)
        elif cmd == u"HME":
            hme = understand_hme_command(sock)
        elif cmd == u"MAP":
            map = understand_upd_command(sock)
            print(">Start mapping")
            for case in map :
                print("case ", case)
                convert_tuple(game,case)
                if case[0] == hme[0] and  case[1] == hme[1] :
                    if case[3] == 0 :
                        game.team_specie = WEREWOLF
        elif cmd == u"UPD":
            upd = understand_upd_command(sock)
            print(upd)
            print("game map before conversion")
            print_map(game)
            for change in upd :
                convert_tuple(game,change)
            print("game map after conversion")
            print_map(game)
            start = time()
            moves = next_moves_decider(game)
            end = time()
            print("Done in {0} seconds".format( end - start))
            # reverse x et y
            #for i in range(len(moves)):
            #   moves[i] = [moves[i][1], moves[i][0], moves[i][2], moves[i][4], moves[i][3]]
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

